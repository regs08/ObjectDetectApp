from mqtt_logic.mqtt_client_base import BaseMQTTClient


class LoggingMQTTClient(BaseMQTTClient):
    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode('utf-8')
        print(f"[LOG] Topic: {msg.topic}, Message: {payload}")
