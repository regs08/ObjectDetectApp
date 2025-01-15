import numpy as np
from PIL import Image
from model_logic.base_classes.preprocessor import PreprocessorBase

class YOLOPreprocessor(PreprocessorBase):
    def __init__(self):
        super().__init__()
        self.input_shape = None
    def initialize(self, input_shape):
        """
        used to intialize in the given model. We intialize it later so we can add the input shape easier
        :param input_shape:
        :return:
        """
        self.input_shape = input_shape
    def load_image(self, image):
        """
        Load an image from a file path or a NumPy array, and return a PIL Image object.
        :param image: Path to an image file or a NumPy array.
        :return: PIL Image object in RGB mode.
        """
        if isinstance(image, str):  # If the input is a file path
            pil_image = Image.open(image).convert("RGB")  # Load and ensure RGB
        elif isinstance(image, np.ndarray):  # If the input is already a NumPy array
            pil_image = Image.fromarray(image)  # Convert to PIL Image
        else:
            raise ValueError("Input must be a file path (str) or a NumPy array.")

        return pil_image

    def preprocess_image(self, image):
        """
        Preprocess the input image, which can be a file path or a NumPy array.
        :param image: Path to an image file or a NumPy array.
        :return: Preprocessed NumPy array ready for inference.
        """
        # Load the image using the helper method
        self.is_initialized()
        loaded_image = self.load_image(image)
        original_dims = loaded_image.size[:2]  # Height, Width

        # Resize the image using PIL to match model input shape
        resized_image = loaded_image.resize(
            (self.input_shape[2], self.input_shape[1]), Image.Resampling.BILINEAR
        )  # Resize to input shape

        # Convert back to NumPy and normalize again
        resized_image = np.asarray(resized_image, dtype=np.float32) / 255.0

        # Ensure it has 3 channels (RGB)
        if resized_image.ndim == 2:  # If grayscale
            resized_image = np.stack((resized_image,) * 3, axis=-1)
        elif resized_image.shape[-1] != 3:
            raise ValueError("Input image must have 3 color channels (RGB).")

        # Expand dimensions to match model input shape
        input_data = np.expand_dims(resized_image, axis=0)  # Add batch dimension

        return input_data, original_dims
