import yaml
import os

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

    def load_nested_config(self, path):
        """Load a nested configuration from the specified YAML file."""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def create_config_object(self, config_type, config_path=None, config_dict=None) -> Config:
        """
        Create a corresponding config object from a YAML file or dictionary.

        Args:
            config_type (str): The type of configuration to create.
            config_path (str, optional): The path to the YAML file for this configuration.
            config_dict (dict, optional): The dictionary to initialize the configuration.

        Returns:
            Config: An instance of the configuration class created by the ConfigFactory.
        """
        if config_path and config_dict:
            raise ValueError("Provide only one of config_path or config_dict, not both.")
        if config_path:
            # Remove nested structure if loading from a file
            config_dict = self.load_config(config_path).get(config_type, {})
        if not config_dict and not config_path:
            raise ValueError("A valid configuration dictionary or path is is required. ")

        config_obj = self.config_factory.create_config(config_type, config_dict)
        config_obj.check_required_params()
        return config_obj
