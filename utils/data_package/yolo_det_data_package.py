from utils.data_package.data_package_base import DataPackage
import numpy as np
import supervision as sv
class YoloDetectionDataPackage(DataPackage):
    def __init__(self, frame=None, detections=None):
        """
        Initialize a YOLO-specific DataPackage.

        Args:
            frame (Any, optional): The frame data. Defaults to None.
            detections (sv.Detections, optional): The YOLO detections object. Defaults to None.
        """
        super().__init__(frame, detections)

    def to_dict(self):
        """
        Convert the YOLO-specific DataPackage to a dictionary format.

        Returns:
            dict: A dictionary with frame and YOLO detection attributes.
        """
        def serialize_array(array):
            """Converts a NumPy array to a list for JSON serialization."""
            return array.tolist() if isinstance(array, np.ndarray) else None

        if self.detections is not None and isinstance(self.detections, sv.Detections):
            return {
                "frame": self.encode_frame_to_base64(),
                "detections": {
                    "xyxy": serialize_array(self.detections.xyxy),
                    "mask": serialize_array(self.detections.mask) if hasattr(self.detections, "mask") else None,
                    "confidence": serialize_array(self.detections.confidence) if hasattr(self.detections, "confidence") else None,
                    "class_id": serialize_array(self.detections.class_id) if hasattr(self.detections, "class_id") else None,
                    "tracker_id": serialize_array(self.detections.tracker_id) if hasattr(self.detections, "tracker_id") else None,
                    "metadata": {
                        key: serialize_array(value) if isinstance(value, np.ndarray) else value
                        for key, value in getattr(self.detections, "metadata", {}).items()
                    } if hasattr(self.detections, "metadata") else {}
                }
            }
        return super().to_dict()
