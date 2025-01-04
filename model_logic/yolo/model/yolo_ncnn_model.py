from model_logic.base_classes.model_base import ModelBase
from utils.configs.config_base import Config
#from ultralytics import YOLO
class YoloNcnnModel(ModelBase):

    def __init__(self):
        super().__init__()
        self.model = None

    def initialize(self, config: Config):
        self.model = YOLO(config.get('model_path'))

    def predict(self, image):
        results = self.model(image)
        return results




