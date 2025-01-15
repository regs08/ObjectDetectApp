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
    @staticmethod
    def load_class_labels(source):
        """
        Load class labels from a file or directly from a list.
        :param source: Either a path to a .txt file or a list of class labels.
        :return: List of class labels.
        """
        if isinstance(source, str):  # If a file path is provided
            if not source.endswith(".txt"):
                raise ValueError("Unsupported file format. Only .txt files are supported.")
            with open(source, "r") as f:
                class_labels = [line.strip() for line in f.readlines()]
        elif isinstance(source, list):  # If a list of labels is provided directly
            class_labels = source
        else:
            raise ValueError("Source must be a file path (str) or a list of labels.")

        self.class_labels = class_labels