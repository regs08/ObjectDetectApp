from queue import Queue, Full, Empty
from app.base_classes.manager import BaseManager
from model_logic.base_classes.model_manager import ModelManager
from stream.stream_types.file_stream import FileStream
from stream.stream_types.http_stream import HTTPStream
from stream.stream_types.camera_stream import CameraStream
import time
import cv2

from utils.data_package.data_package_base import DataPackage
from utils.data_package.yolo_det_data_package import YoloDetectionDataPackage


class StreamManager(BaseManager):
    """
    A class for handling real-time video streaming from a given stream source.

    This class uses a `current_stream` object to capture video frames and process them in real time.
    It manages the stream in a separate thread and stores frames in a queue for further processing.
    """

    def __init__(self):
        """
        Initializes the StreamHandler with a given stream source.

        Parameters:
        - current_stream: An object that handles the stream operations (e.g., open, read, close).
        """
        super().__init__()
        self.current_stream = None
        self.stream_type = None
        self.source = None
        self.running = False
        self.output_queue = Queue(maxsize=10)

    def initialize(self, config):
        """
        pass in the params for the stream manager object
        :param stream_type: Type of stream (e.g., 'http', 'camera', 'file').
        :param source: The source of the stream.
        :param model_manager: The model to use for processing.
        """
        self.populate_with_config(config)

        if self.current_stream:
            self.current_stream.close()

        if self.stream_type == "http":
            self.current_stream = HTTPStream(self.source)
        elif self.stream_type == "camera":
            self.current_stream = CameraStream(self.source)
        elif self.stream_type == "file":
            self.current_stream = FileStream(self.source)
        else:
            raise ValueError(f"Unsupported stream type: {self.stream_type}")

    def populate_with_config(self, config: dict):
        """
        Initialize StreamManager using a configuration dictionary.
        :param config: Configuration dictionary containing 'stream_type' and 'source'.
        :param model_manager: The model manager for processing frames.
        """
        self.stream_type = config.get("stream_type")
        self.source = config.get("source")


    def run(self, inference_model: ModelManager=None):
        """
        Captures video frames and stores them in a queue.
        """
        self.current_stream.open()  # Open the stream source
        self.running = True
        while self.running:
            if not self.current_stream.cap.isOpened():
                print("Stream disconnected, attempting to reconnect.")
                try:
                    self.current_stream.cap.open()
                except ConnectionError as e:
                    print(f"Reconnection failed: {e}")
                    time.sleep(2)
                    continue

            frame = self.current_stream.read_frame()
            if frame is None:
                print("Frame read failed, skipping frame.")
                time.sleep(0.1)
                continue
            if inference_model:
                data_package = inference_model.run(frame)
            else:
                data_package = YoloDetectionDataPackage(frame)
            # Push frame into the output queue
            try:
                self.output_queue.put_nowait(data_package)
            except Full:
                print("Output queue is full, dropping frame.")

        self.current_stream.close()  # Close the stream source when streaming stops

    def display_stream(self, annotated_frame=None):
        """
        Continuously display frames from the output queue or a test frame.

        Parameters:
        - test_frame: Optional. A single frame (numpy array) to test and display.
        - model: Optional. A model instance to process the frame with.
        """
        print("Displaying stream. Press 'q' to exit.")
        while self.running or annotated_frame is not None:
            try:
                # Use the test frame if provided
                data = annotated_frame if annotated_frame is not None else self.output_queue.get(timeout=1)
                if isinstance(data, DataPackage):
                    frame = data.frame

                # Display the frame (annotated or raw)
                cv2.imshow("Stream Window", data)

                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break

                # For testing, exit after displaying the test frame once
                if annotated_frame is not None:
                    break
            except Empty:
                print("No frames available in the queue.")
                time.sleep(0.1)

        cv2.destroyAllWindows()

    def set_name(self):
        self.name = "StreamManager"