from app.base_classes.manager import BaseManager
import time
import cv2
from queue import Empty, Queue
import threading

from model_logic.base_classes.model_manager import ModelManager
from utils.factories.model_manager_factory import ModelManagerFactory

from utils.data_package.yolo_det_data_package import YoloDetectionDataPackage
from mqtt_logic.mqtt_manager import MQTTManager
from stream.stream_manager import StreamManager
from utils.configs.config_manager import ConfigManager
from utils.data_package.data_package_base import DataPackage
from utils.configs.all_configs import AppManagerConfig, ModelManagerConfig, StreamManagerConfig, \
    MqttManagerConfig


class AppManager(BaseManager):
    """
    Centralized manager to handle multiple BaseManager instances.
    """

    def __init__(self):
        """
        Initialize the AppManager with optional model and stream managers.
        """
        super().__init__()
        self.config = AppManagerConfig()
        self.config_manager = ConfigManager()

        # type of model manager. define the type from config
        self.model_manager = ModelManager
        self.model_manager_config = ModelManagerConfig()

        self.stream_manager = StreamManager()
        self.stream_manager_config = StreamManagerConfig()

        self.mqtt_manager = MQTTManager()
        self.mqtt_manager_config = MqttManagerConfig()

        self.inference_running = False
        self.detection_queue = Queue(maxsize=10)
        self.stream_thread = None
        self.output_thread = None

    def run(self):
        # starts inference thread
        self.start_inference()
        # starts mqtt client thread
        self.mqtt_manager.run()
        # starts the mqtt pakcage send
        self.mqtt_manager.start_batching(batch_size=10,
                                         batch_interval=5,
                                         get_data_fn=self.get_inference_data)

    def initialize(self, config_path):
        """
        Load configuration and initialize managers.
        """
        self.create_and_check_config_objects(config_path)
        self.initialize_managers()

    def initialize_managers(self):

        manager_type = self.model_manager_config.get("type")
        self.model_manager = ModelManagerFactory.create_model_manager(manager_type)

        self.model_manager.initialize(self.model_manager_config)
        self.stream_manager.initialize(self.stream_manager_config)
        self.mqtt_manager.initialize(self.mqtt_manager_config)

    def create_and_check_config_objects(self, config_path):
        """
        method to encapsualte the loading of configs. on creation the config base checks the required params
        :param config_path:
        :return:
        """
        self.config = self.config_manager.create_config_object(config_type="AppManager",
                                                               config_path=config_path)

        self.model_manager_config = self.config_manager.create_config_object(
            config_type="ModelManager",
            config_path=self.config.get('ModelManager'))

        self.stream_manager_config = self.config_manager.create_config_object(
            config_type="StreamManager",
            config_path=self.config.get('StreamManager'))

        self.mqtt_manager_config = self.config_manager.create_config_object(
            config_type="MqttManager",
            config_path=self.config.get('MqttManager')
        )
    def set_name(self):
        self.name = "AppManager"

    def start_inference(self):
        """
        Start the inference process through the InferenceManager.
        """
        self.inference_running = True

        # Threads for stream management and output processing we pass in model manager for inference
        self.stream_thread = threading.Thread(target=self.stream_manager.run, args=(self.model_manager,))
        self.output_thread = threading.Thread(target=self._process_output)

        # Start the threads
        self.stream_thread.start()
        self.output_thread.start()

    def _process_output(self):
        """
        Process frames from the StreamManager and send to the output queue.
        """
        while self.running:
            try:
                # Get annotated frames or data packages from the stream's output queue
                data_package = self.stream_manager.output_queue.get(timeout=1)
                # Push to the output queue for AppManager
                self.detection_queue.put(data_package)

            except Empty:
                print("Output queue is empty.")
            except Exception as e:
                print(f"Error processing output: {e}")

    def stop(self):
        """
        Stop the streaming and inference process.
        """
        self.running = False
        self.stream_manager.running = False
        if self.stream_thread.is_alive():
            self.stream_thread.join()
        if self.output_thread.is_alive():
            self.output_thread.join()

    def get_inference_data(self):
        try:
            data_package = self.detection_queue.get(timeout=1)
            data_package = data_package.to_dict()
            # just sending detections obejct for testing now
            return data_package['detections']
        except Empty:
            print("Empty inference queue..")
        return DataPackage.empty().to_dict()


    def display_stream(self, annotated_frame=None):
        """
        Continuously display frames from the output queue or a test frame.

        Parameters:
        - test_frame: Optional. A single frame (numpy array) to test and display.
        - model: Optional. A model instance to process the frame with.
        """
        print("Displaying stream. Press 'q' to exit.")
        while self.running:
            try:
                # Use the test frame if provided
                frame = self.detection_queue.get(timeout=1)
                if isinstance(frame, YoloDetectionDataPackage):
                    frame = frame.frame

                if frame is None:
                    print("Frame read failed, skipping frame.")
                    time.sleep(0.5)
                    continue

                # Display the frame (annotated or raw)
                cv2.imshow("Stream Window", frame)

                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break

            except Empty:
                print("No frames available in the queue.")
                time.sleep(1)

        cv2.destroyAllWindows()

