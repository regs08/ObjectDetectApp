from utils.configs.config_base import Config

class AppManagerConfig(Config):
    def __init__(self, **kwargs):
        """
        Initialize the AppManagerConfig with additional attributes.

        Args:
            **kwargs: Arbitrary keyword arguments to initialize attributes directly.
        """
        super().__init__(**kwargs)
        self.required_params = ['ModelManager', 'StreamManager', 'MqttManager']

class MqttManagerConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_params = ["host", "port", "topic"]


class StreamManagerConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_params = ["source", "stream_type"]

class ModelManagerConfig(Config):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.required_params = ["model", "model_path", "confidence_threshold", "class_labels",
                                "annotator"]
