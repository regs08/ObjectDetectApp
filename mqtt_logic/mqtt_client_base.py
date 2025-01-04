from abc import ABC, abstractmethod
import paho.mqtt.client as mqtt
import json

class BaseMQTTClient(ABC):
    def __init__(self):
        self.host = None
        self.port = None
        self.topic = None
        self.client = mqtt.Client()

    def initialize(self, config):
        self.populate_with_config(config)

    def populate_with_config(self, config):
        """
        assign class params
        """

        self.host = config.get("host")
        self.port = config.get("port")
        self.topic = config.get("topic")

    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message  # Attach subclass-specific `on_message`
        self.client.connect(self.host, self.port, 60)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT broker at {self.host}:{self.port}")
            client.subscribe(self.topic)
        else:
            print(f"Failed to connect, return code {rc}")

    @abstractmethod
    def on_message(self, client, userdata, msg):
        """
        Abstract method to handle incoming messages.
        Must be implemented by subclasses.
        """
        pass

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()
        print("Disconnected from MQTT broker")

    def publish(self, data):
        payload = json.dumps(data)
        self.client.publish(self.topic, payload)
        #print(f"Published: {payload}")