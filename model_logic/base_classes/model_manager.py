from annotator.detections.detections_annotator import FrameAnnotatorDetections
from app.base_classes.manager import BaseManager
from model_logic.yolo.model.yolo_ncnn_model import YoloNcnnModel
from utils.configs.config_base import Config
from model_logic.yolo.model.yolo_model import YOLOModel
import numpy as np

from utils.data_package.yolo_det_data_package import YoloDetectionDataPackage


class ModelManager(BaseManager):
    def __init__(self):
        super().__init__()

        self.model_path = None
        self.class_labels = None
        self.preprocessor = None
        self.postprocessor = None
        self.annotator = None
        self.model_factory = {'YoloModel': YOLOModel,
                              'YoloNCNNModel': YoloNcnnModel,}
        self.annotator_factory = {'DetectionAnnotator': FrameAnnotatorDetections}
        self.confidence_threshold = None
        self.model = None

    def initialize(self, *args):
        """
        intialize the model's compenentents, pre/post processor
        :param args:
        :return:
        """
        pass

    # def set_pre_post_processors(self, *args):
    #     raise NotImplementedError ("must implement set post and preprocessor")

    def populate_with_config(self, config: Config):
        """
        Intialize ModelManager with specific configurations.
        """
        # Create model instance dynamically (using a factory or import logic)
        self.model = self.model_factory[config.get('model')]()
        self.model_path = config.get("model_path")
        self.confidence_threshold =config.get("confidence_threshold")
        self.class_labels = config.get("class_labels")
        self.annotator = self.annotator_factory[config.get("annotator")]()

    def set_name(self):
        self.name = "ModelManager"

    def utils_defined(self):
        if self.preprocessor is None or self.postprocessor is None or self.annotator is None:
            return False
        else:
            return True

    def run(self, frame: np.ndarray):
        """
        Main thread logic for processing frames.
        """
        try:
            #run inference
            detections = self.model.predict(frame)
            #annotate frame
            # if no detections just the orig frame is returned
            annotated_frame = self.annotator.annotate_frame(detections, frame)
            #create data package
            data_package = YoloDetectionDataPackage(detections=detections,
                                       frame=annotated_frame)

            return data_package
        except Exception as e:
            print(f"ModelManager error: {e}")

