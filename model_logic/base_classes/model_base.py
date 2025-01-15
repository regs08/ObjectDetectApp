from abc import ABC, abstractmethod

class ModelBase(ABC):
    def __init__(self,):
        self.labels = None
        self.model_path = None
        self.config = None
        self.confidence_threshold = None
    @abstractmethod
    def initialize(self, *args):
        pass
    @abstractmethod
    def predict(self, image):
        """
        Perform inference on the provided image, which can be either a file path or a NumPy array.
        :param image: Path to an image file or a NumPy array representing the image.
        :return: Predictions in human-readable format.
        """
        pass