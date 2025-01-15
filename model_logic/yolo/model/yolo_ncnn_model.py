from annotator.frame_annotator_base import FrameAnnotatorBase
from model_logic.base_classes.model_base import ModelBase
from utils.configs.config_base import Config
from ultralytics import YOLO

class YoloNcnnModel(ModelBase):

    def __init__(self):
        super().__init__()
        self.model = None
    def initialize(self, config: Config):
        self.model_path = config.get("model_path")
        self.labels = config.get("labels")
        self.confidence_threshold = config.get("confidence_threshold")
        self.model = YOLO(self.model_path)
    def predict(self, image):
        results = self.model(image)
        return results




