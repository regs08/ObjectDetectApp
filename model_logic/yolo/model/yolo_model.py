from ai_edge_litert.interpreter import Interpreter
from model_logic.base_classes.model_base import ModelBase
import cv2
from supervision.detection.core import Detections

from model_logic.yolo.postprocessing.yolo_postprocessor import YOLOPostprocessor
from model_logic.yolo.preprocessing.yolo_preprocessor import YOLOPreprocessor
from utils.data_package.yolo_det_data_package import YoloDetectionDataPackage


class YOLOModel(ModelBase):
    def __init__(self):
        """
        Initialize the Model without loading the interpreter immediately.
        :param preprocessor: An instance of the Preprocessor class.
        :param postprocessor: An instance of the PostProcessor class.
        """
        super().__init__()
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.preprocessor = YOLOPreprocessor()
        self.postprocessor = YOLOPostprocessor()
        self.data_package_type = YoloDetectionDataPackage

    def initialize(self, model_path,
                   class_labels):
        """
        Load the TFLite interpreter and initialize the input/output details.
        :param model_path: Path to the TFLite model file.
        """

        self.interpreter = Interpreter(model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.preprocessor.initialize(self.input_details[0]['shape'])
        self.postprocessor.initialize(class_labels)

    def predict(self, image, is_video=False)-> Detections:
        """
        Perform inference on the provided image.
        :param image: Path to the image to be processed.
        :return: detections in super vision format.
        """
        if not self.interpreter:
            raise ValueError("Interpreter is not initialized. Call `initialize` first.")

        image, orginal_dims = self.preprocessor.preprocess_image(image)
        #input_size = self.input_details[0]['shape'][1]
        if is_video:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Set the tensor with the preprocessed image
        self.interpreter.set_tensor(self.input_details[0]['index'], image)

        # Invoke the interpreter to run inference
        self.interpreter.invoke()

        # Retrieve the output data
        output_data = [self.interpreter.get_tensor(detail['index']) for detail in self.output_details]

        # Postprocess the output data
        predictions = self.postprocessor.postprocess(output_data, orginal_dims)
        return predictions

