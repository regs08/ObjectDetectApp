import json
import paho.mqtt.client as mqtt

class MQTTClient:
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

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT broker at {self.host}:{self.port}")
            client.subscribe(self.topic)
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(self, client, userdata, msg):
        #print(f"Received message on topic '{msg.topic}': {msg.payload.decode()}")
        pass

    def connect(self):
        # Set up MQTT callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the broker
        self.client.connect(self.host, self.port, 60)
        print(f"Connecting to MQTT broker at {self.host}:{self.port}...")

    def publish(self, data):
        payload = json.dumps(data)
        self.client.publish(self.topic, payload)
        #print(f"Published: {payload}")

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()
        print("Disconnected from MQTT broker")
