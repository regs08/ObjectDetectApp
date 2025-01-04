from mqtt_logic.mqtt_client_base import BaseMQTTClient

class SenderMQTTClient(BaseMQTTClient):
    def on_message(self, client, userdata, msg):
        pass