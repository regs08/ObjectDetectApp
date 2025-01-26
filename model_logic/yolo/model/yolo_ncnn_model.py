from model_logic.base_classes.model_base import ModelBase
from utils.configs.config_base import Config
from ultralytics import YOLO

class YoloNcnnModel(ModelBase):

    def __init__(self):
        super().__init__()
        self.model = None
        self.task = None
    def initialize(self, config: Config):
        self.model_path = config.get("model_path")
        self.labels = config.get("labels")
        self.task = config.get("task")
        self.confidence_threshold = config.get("confidence_threshold")
        self.model = YOLO(self.model_path, task=self.task)
    def predict(self, image):
        results = self.model(image, verbose=False)
        return results




