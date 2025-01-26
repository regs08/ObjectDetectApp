import yaml

from utils.factories.config_factory import ConfigFactory
from utils.configs.config_base import Config

class ConfigManager:
    def __init__(self):
        """
        Initialize the ConfigManager with a YAML configuration file.

        Args:
        """
        self.config_factory = ConfigFactory()

    def load_config(self, config):
        """Load the main configuration from the YAML file."""
        with open(config, 'r') as f:
            return yaml.safe_load(f)

    def create_config_object(self, config_path=None, config_dict=None) -> Config:
        """
        Create a corresponding config object from a YAML file or dictionary.

        Args:
            config_path (str, optional): The path to the YAML file for this configuration.
            config_dict (dict, optional): The dictionary to initialize the configuration.

        Returns:
            Config: An instance of the configuration class created by the ConfigFactory.

        Raises:
            ValueError: If neither `config_path` nor `config_dict` is provided, or if the `type` field is missing.
        """
        if not config_path and not config_dict:
            raise ValueError("Provide either `config_path` or `config_dict`.")
        # Load configuration from file if a path is provided
        if config_path:
            try:
                config_dict = self.load_config(config_path)
            except Exception as e:
                raise ValueError(f"Failed to load configuration from {config_path}: {e}")

        # Validate and extract the config type
        if not isinstance(config_dict, dict):
            raise ValueError("The configuration must be a dictionary.")
        config_type = config_dict['type']
        if not config_type:
            raise ValueError("The `type` field is missing from the configuration.")

        # Create and return the configuration object
        return self.config_factory.create_config(config_type, config_dict)


