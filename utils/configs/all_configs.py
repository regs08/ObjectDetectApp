from utils.configs.config_base import Config

class AppManagerConfig(Config):
    def __init__(self, **kwargs):
        """
        Initialize the AppManagerConfig with additional attributes.

        Args:
            **kwargs: Arbitrary keyword arguments to initialize attributes directly.
        """
        super().__init__(**kwargs)
        self.required_keys = ['ModelManager', 'StreamManager', 'MqttManager']

class MqttManagerConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_keys = ["client_types"]

class StreamManagerConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_keys = ["source", "stream_type"]

class ModelManagerConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_keys = ["model_config_path"]
class YoloNCNNConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_keys = ["model_path", "confidence_threshold", "class_labels",
                                "type", "preprocessor", "postprocessor", 'task']
class MqttClientConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_keys = ["client_types"]