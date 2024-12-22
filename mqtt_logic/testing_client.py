from mqtt_logic.mqtt_manager import MQTTManager
from utils.mock_data_package import test_data_package
import time
def test_mqtt_manager():
    config_file = "/assets/old_configs/mqtt_config.json"
    mqtt_manager = MQTTManager()
    mqtt_manager.initialize(config_file)



    mqtt_manager.run()

    # Start batching with dummy data
    print("\nStarting batching...")
    mqtt_manager.start_batching(batch_size=5, batch_interval=3, get_data_fn=test_data_package)

    # Simulate the system running for a while
    time.sleep(10)

    # Stop batching and MQTTManager
    print("\nStopping batching...")
    mqtt_manager.stop_batching()

    print("Stopping MQTTManager...")
    mqtt_manager.stop()

    print("\nTest completed!")


if __name__ == "__main__":
    test_mqtt_manager()
