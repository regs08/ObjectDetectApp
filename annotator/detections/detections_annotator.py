
import numpy as np
import supervision as sv
from annotator.frame_annotator_base import FrameAnnotatorBase

class FrameAnnotatorDetections(FrameAnnotatorBase):
    def __init__(self):

        super().__init__()  # Initialize the superclass with the results
        self.box_annotator = None
        self.label_annotator = None

    def annotate_frame(self, detections: sv.Detections, scene: np.ndarray, labels) -> np.ndarray:
        """
        Annotate the given frame with detection information.
        :param detections: sv.Detections
        :param scene: The frame to be annotated.
        :param labels: list or txt file of labels
        :return: The frame with annotations (bounding boxes and labels).
        """
        if not isinstance(detections, sv.Detections):
            raise TypeError("Error in Frame Annotator: results not of Supervision Detection")
        # Calculate and display the frames per second on the frame

        # Check if there are any detections to annotate
        if len(detections.xyxy) > 0:
            # Annotate the frame with bounding boxes and labels
            annotated_frame = self.box_annotator.annotate(scene, detections)
            annotated_frame = self.label_annotator.annotate(annotated_frame, detections, labels=labels)
            # Return the annotated frame
            return annotated_frame

        # If no detections, return the original frame
        return scene
    def initialize(self):
        self.box_annotator = sv.BoxAnnotator()
        self.label_annotator = sv.LabelAnnotator(text_position=sv.Position.TOP_RIGHT)
