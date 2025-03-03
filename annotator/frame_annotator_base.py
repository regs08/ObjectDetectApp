from abc import ABC, abstractmethod

import numpy as np
import supervision as sv
class FrameAnnotatorBase(ABC):
    def __init__(self):
        """
        Initialize the frame_annotator with a FPSUtility instance.

        :param fps_utility: An instance of FPSUtility to calculate and display frames per second.
        """
        self.is_initialized = False

    @abstractmethod
    def annotate_frame(self,frame: np.ndarray, detections: sv.Detections, labels):
        """
        Abstract method to annotate a frame.
        This method must be implemented by subclasses of frame_annotator.

        :param detections: results obtained from a model
        :param frame: The frame to be annotated.

        """
        pass
    @abstractmethod
    def initialize(self):
        """
        abstract method to initialize the frame_annotator
        :return:
        """



