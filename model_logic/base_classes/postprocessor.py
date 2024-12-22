from abc import ABC, abstractmethod

class PostprocessorBase(ABC):
    def __init__(self, class_labels=None, conf_threshold=0.3, ):
        """
        Initialize the PostProcessor with class labels and a confidence threshold.
        :param class_labels: List of class labels or None if using a file to load labels.
        :param conf_threshold: Confidence threshold for filtering predictions.
        """
        self.class_labels = class_labels
        self.conf_threshold = conf_threshold

    @staticmethod
    @abstractmethod
    def load_class_labels(source):
        """
        Abstract method to load class labels from a file or directly from a list.
        :param source: Either a path to a .txt file or a list of class labels.
        :return: List of class labels.
        """
        pass

    @abstractmethod
    def process_output(self, output_data, orginal_dims):
        """
        Abstract method to process the model's raw output into human-readable predictions.
        :param output_data: Raw output from the model.
        :return: List of predictions (label, confidence).
        """
        pass
    def initialize(self, class_labels):
        self.load_class_labels(class_labels)



