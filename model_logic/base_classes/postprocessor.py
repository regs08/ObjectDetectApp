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

    def load_class_labels(self, source):
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

    @abstractmethod
    def postprocess(self, **args):
        """
        Abstract method to process the model's raw output into human-readable predictions.
        :param args: Raw output from the model.
        :return: List of predictions (label, confidence).
        """
        pass
    def annotate_frame(self, frame, detections, annotator):
        raise NotImplementedError("Must implement annotate frame in postprocessor.")
    def initialize(self, class_labels):
        self.load_class_labels(class_labels)



