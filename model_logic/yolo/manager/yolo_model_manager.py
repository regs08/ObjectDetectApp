from model_logic.base_classes.model_manager import ModelManager
from model_logic.yolo.preprocessing.yolo_preprocessor import YOLOPreprocessor
from model_logic.yolo.postprocessing.yolo_postprocessor import YOLOPostprocessor
from utils.configs.config_base import Config

class YoloModelManager(ModelManager):

    def __init__(self, ):
        super().__init__()

    def initialize(self, config):

        # loads the config in json or dict format
        # populates the class variables

        self.set_pre_post_processors()
        self.populate_with_config(config)
        # intialization happens in model class, pre and post processor definitions is dependent on the model
        self.model.initialize(self.model_path,
                              class_labels=self.class_labels,
                              preprocessor=self.preprocessor,
                              postprocessor=self.postprocessor)
        self.annotator.initialize()

        if not self.utils_defined():
            raise NotImplementedError('Model utils not implemented.')

    def populate_with_config(self, config: Config):
        """
        Intialize ModelManager with specific configurations.
        """
        # Create model instance dynamically (using a factory or import logic)
        self.model = self.model_factory[config.get('model')]()  # Example factory
        self.model_path = config.get("model_path")
        self.confidence_threshold =config.get("confidence_threshold")
        self.class_labels = config.get("class_labels")
        self.annotator = self.annotator_factory[config.get("annotator")]()

    def set_pre_post_processors(self):
        self.preprocessor = YOLOPreprocessor()
        self.postprocessor = YOLOPostprocessor()
