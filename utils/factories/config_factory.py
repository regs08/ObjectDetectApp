from utils.configs.all_configs import *  # Importing all required old_configs

class ConfigFactory:
    """
    A factory class for creating configuration objects based on a specified type.
    """
    def __init__(self):
        """
        Initialize the ConfigFactory with a mapping of configuration names to their respective classes.
        """
        self.configs = {
            "AppManager": AppManagerConfig,
            "StreamManager": StreamManagerConfig,
            "ModelManager": ModelManagerConfig,
            "MqttManager": MqttManagerConfig,
            "YoloNCNNModel": YoloNCNNConfig,
        }

    def create_config(self, config_type, config_dict: dict) -> Config:
        """
        Create a configuration object of the specified type using a dictionary.

        Args:
            config_type (str): The type of configuration to create (e.g., "AppManager").
            config_dict (dict): A dictionary of configuration parameters.

        Returns:
            object: An instance of the specified configuration class.

        Raises:
            ValueError: If the specified config_type is not supported.
        """
        if config_type not in self.configs:
            raise ValueError(f"Unsupported configuration type: {config_type}")

        config_class = self.configs[config_type]
        return config_class(**config_dict)
