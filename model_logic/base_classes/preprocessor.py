from abc import ABC, abstractmethod

from tensorflow.python.distribute.multi_process_runner import NotInitializedError


class PreprocessorBase(ABC):
    def __init__(self):
        self.input_shape = None
    def initialize(self, input_shape):
        """
        used to intialize in the given model. We intialize it later so we can add the input shape easier
        :param input_shape:
        :return:
        """
        self.input_shape = input_shape
    def is_initialized(self):
        if self.input_shape is None:
            raise NotInitializedError ("Input shape is not initialized. Call the initialize method")
    @abstractmethod
    def load_image(self, image):
        """
        Abstract method to load an image from a file path or a NumPy array.
        :param image: Path to an image file or a NumPy array.
        :return: PIL Image object.
        """
        pass

    @abstractmethod
    def preprocess_image(self, image):
        """
        Abstract method to preprocess the input image.
        :param image: Path to an image file or a NumPy array.
        :return: Preprocessed NumPy array ready for inference.
        """
        pass

