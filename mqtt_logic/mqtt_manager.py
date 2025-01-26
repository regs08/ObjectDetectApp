from app.base_classes.manager import BaseManager
from utils.configs.config_base import Config
from utils.factories.mqtt_client_factory import MqttClientFactory
import threading
from queue import Empty
import time
import json

from utils.configs.config_manager import ConfigManager

class MQTTManager(BaseManager):
    def __init__(self):
        """
        Initialize the MQTTManager with an MQTTClient instance.
        """
        super().__init__()
        self.mqtt_client = None
        self.client = None

        self.is_connected = False
        self.config_manager = ConfigManager()
        # Thread management
        self._stop_event = threading.Event()
        self.batching_thread = None
        self.client_factory = MqttClientFactory()

    def initialize(self, mqtt_config: Config, client_type):

        config_path = mqtt_config.get('sender')
        mqtt_config = self.config_manager.create_config_object(config_path=config_path)
        # get the client type from the config

        # create client class from config type
        self.mqtt_client = self.client_factory.clients[client_type]()
        # assign the class' client to the managers client for readability
        self.client = self.mqtt_client.client

        # initialize client
        print('Loading', mqtt_config)
        self.mqtt_client.initialize(mqtt_config)

    def run(self):
        """
        Start the MQTT client connection and loop.
        """
        try:
            self.mqtt_client.connect()
            self.mqtt_client.loop_start()
            self.is_connected = True
            print("MQTTManager: Started MQTT client.")
        except Exception as e:
            print(f"MQTTManager: Failed to start MQTT client. Error: {e}")
            self.is_connected = False


    def stop(self):
        """
        Stop the MQTT client connection and loop.
        """
        if self.is_connected:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
            self.is_connected = False
            print("MQTTManager: Stopped MQTT client.")

    def publish_batch(self, batch):
        """
        Serialize and publish an entire batch of data packages via MQTT as a single payload.
        """
        if not self.is_connected:
            print("MQTTManager: Cannot publish batch, MQTT client is not connected.")
            return

        try:
            # Serialize the entire batch to a JSON string
            batch_payload = json.dumps(batch)
            self.mqtt_client.publish(batch_payload)
            print(f"MQTTManager: Published batch with {len(batch)} items.")
        except Exception as e:
            print(f"MQTTManager: Failed to publish batch. Error: {e}")

    def publish_data_package(self, data_package):
        """
        (Optional) Serialize and publish a single data package via MQTT.
        Retained for backward compatibility or specific use cases.
        """
        if not self.is_connected:
            print("MQTTManager: Cannot publish, MQTT client is not connected.")
            return

        try:
            # Ensure data_package is serialized
            if not isinstance(data_package, dict):
                data_package = data_package.to_dict()
            payload = json.dumps(data_package)
            self.mqtt_client.publish(payload)
            print(f"MQTTManager: Published single data package.")
        except Exception as e:
            print(f"MQTTManager: Failed to publish data package. Error: {e}")

    def set_name(self):
        self.name = "MQTTManager"

    def send_batch_data(self, batch_size=10, batch_interval=5, get_data_fn=None):
        batch = []  # Initialize the batch
        start_time = time.time()

        while not self._stop_event.is_set():  # Check the stop event to exit the loop
            try:

                # Add detection data to the batch
                data_package = get_data_fn()
                assert isinstance(data_package, dict), "data package must be a dict "
                batch.append(data_package)
                # Check if batch is ready to be sent
                if len(batch) >= batch_size or (time.time() - start_time) >= batch_interval:
                    self.publish_batch(batch)
                    print(f"Published batch of size: {len(batch)}")

                    # Reset the batch and timer
                    batch = []
                    start_time = time.time()

            except Empty:
                print("Empty queue, waiting for inference...")

            except Exception as e:
                print(f"Error during inference batching: {e}")

    def start_batching(self, batch_size=10, batch_interval=5, get_data_fn=None):
        """
        Start the batching and MQTT publishing logic in a separate thread.
        """
        self._stop_event.clear()
        self.batching_thread = threading.Thread(
            target=self.send_batch_data,
            args=(batch_size, batch_interval, get_data_fn),
            daemon=True
        )
        self.batching_thread.start()

    def stop_batching(self):
        """
        Stop the batching thread.
        """
        self._stop_event.set()
        if self.batching_thread:
            self.batching_thread.join()
            self.batching_thread = None