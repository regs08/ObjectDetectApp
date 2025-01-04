from mqtt_logic.logger_mqtt_client import LoggingMQTTClient
from mqtt_logic.sender_mqtt_client import SenderMQTTClient


class MqttClientFactory:
    def __init__(self):
        self.clients = {
            'sender': SenderMQTTClient,
            'logger': LoggingMQTTClient
        }