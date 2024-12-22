from model_logic.base_classes.model_base import ModelBase

class YoloNcnnModel(ModelBase):

    def __init__(self):
        super().__init__()

    def initialize(self, config):
        pass

    def predict(self, image):
        pass

    def _populate_with_config(self, config):
         self.config = self.config_loader.initialize_config(config)[0]
         self.config = self.config['params']

         model = self.config.get("model")
         model_path = self.config.get("model_path")
         class_labels = self.config.get("class_labels")
         annotator = self.config.get("annotator")
         confidence_threshold = self.config.get("confidence_threshold")

         if not model:
             raise ValueError("YoloNcnnModel requires a 'model' parameter.")
         if not model_path:
             raise ValueError("YoloNcnnModel requires a 'model_path' parameter.")
         if not class_labels:
             raise ValueError("YoloNcnnModel requires a 'class_labels' parameter.")
         if not annotator:
             raise ValueError("YoloNcnnModel requires a 'annotator' parameter.")
         if not confidence_threshold:
             raise ValueError("YoloNcnnModel requires a 'model' parameter.")




