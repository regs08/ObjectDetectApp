import numpy as np
import cv2
import base64

class DataPackage:
    def __init__(self, frame=None, detections=None):
        """
        Initialize a generic DataPackage.

        Args:
            frame (Any, optional): The frame data. Defaults to None.
            detections (Any, optional): The detections data. Defaults to None.
        """
        self.frame = frame
        self.detections = detections

    @staticmethod
    def empty():
        """
        Creates and returns an empty DataPackage.

        Returns:
            DataPackage: An instance of DataPackage with no frame or detections.
        """
        return DataPackage()

    def is_empty(self):
        """
        Checks if the DataPackage is empty.

        Returns:
            bool: True if both frame and detections are empty, False otherwise.
        """
        return self.frame is None and self.detections is None

    def to_dict(self):
        """
        Convert the DataPackage to a dictionary format.

        Returns:
            dict: A dictionary with frame and detections attributes.
        """
        return {
            "frame": self.frame,
            "detections": self.detections,
        }

    def encode_frame_to_base64(self):
        """
        Encodes the frame to a Base64 string if it is a numpy array.

        Returns:
            str: Base64 encoded string of the frame, or None if no frame.
        """
        if self.frame is None:
            return None

        if not isinstance(self.frame, np.ndarray):
            raise TypeError("Frame must be a numpy array.")

        _, buffer = cv2.imencode('.jpg', self.frame)
        return base64.b64encode(buffer).decode('utf-8')

    def __repr__(self):
        return f"DataPackage(frame={self.frame}, detections={self.detections})"
