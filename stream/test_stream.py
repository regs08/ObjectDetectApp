
from model_logic.yolo.manager.yolo_model_manager import YoloModelManager
from stream.stream_manager import StreamManager


model_config_path = "/assets/old_configs/yolo_det_model_config.json"

# Test configuration
test_config = {
    "stream_type": "camera",  # Simulate camera stream
    "source": 0  # 0 is usually the default webcam
}

# Initialize the StreamManager
stream_manager = StreamManager()
model_manager = YoloModelManager()
import json

stream_manager.initialize(test_config)
model_manager.initialize(json.load(open(model_config_path)))

from threading import Thread

stream_manager.running = True
stream_thread = Thread(target=stream_manager.run, args=(model_manager,), daemon=True)
stream_thread.start()
# Display live stream with model
try:
    stream_manager.display_stream()
except KeyboardInterrupt:
    print("Stream interrupted.")
    stream_manager.running = False
finally:
    stream_thread.join()

print("Stream stopped.")
