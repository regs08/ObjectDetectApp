from app.base_classes.manager import BaseManager
from utils.configs.config_base import Config
import numpy as np

from utils.data_package.yolo_det_data_package import YoloDetectionDataPackage
from utils.factories.model_factory import ModelFactory
from utils.factories.processor_factory import ProcessorFactory


class ModelManager(BaseManager):
    def __init__(self):
        super().__init__()

        self.preprocessor = None
        self.postprocessor = None
        self.annotator = None
        self.model_factory = ModelFactory()
        self.processor_factory = ProcessorFactory()
        self.model_config = None
        self.confidence_threshold = None
        self.model = None
        self.model_config_path = None

    def initialize(self, config: Config):
        """
        intialize the model's compenentents, pre/post processor
        :param config:
        :return:
        """
        self.apply_config(config)
        self.model.initialize(config=self.model_config)
        self.preprocessor.initialize()
        self.postprocessor.initialize(self.model_config.get("class_labels"))
        self.annotator.initialize()


    def apply_config(self, config: Config):
        self.model_config_path = config.get("model_config_path")
        # Creating Config object to be passed into our model object
        self.model_config = self.config_manager.create_config_object(config_path=self.model_config_path)
        # Getting type of model from config
        self.model = self.model_factory.models[self.model_config.get("type")]()
        # setting pre and post processors
        # For now the prepocessing is handled by ultralytics. Delete if we don't need or only working with ultra
        self.preprocessor = self.processor_factory.processors[self.model_config.get("preprocessor")]()
        self.postprocessor = self.processor_factory.processors[self.model_config.get("postprocessor")]()
        # setting annotator
        self.annotator = self.annotator_factory.annotators[self.model_config.get("annotator")]()

    def set_name(self):
        self.name = "ModelManager"

    def run(self, frame: np.ndarray):
        """
        Main thread logic for processing frames.
        """
        try:
            # preprocess frame
            preprocessed_frame = self.preprocessor.preprocess_image(frame)
            #run inference
            results = self.model.predict(preprocessed_frame)
            #annotate frame
            # postprocess Frame
            detections = self.postprocessor.postprocess(results[0])
            # if no detections just the orig frame is returned
            annotated_frame = self.annotator.annotate_frame(scene=frame,
                                                            detections=detections,
                                                            labels=self.model.labels)

            #create data package
            data_package = YoloDetectionDataPackage(detections=detections,
                                       frame=annotated_frame)

            return data_package
        except Exception as e:
            print(f"ModelManager error: {e}")

