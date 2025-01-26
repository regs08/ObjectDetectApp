from utils.components.named_entity import NamedEntity

class Config(NamedEntity):
    def __init__(self, **kwargs):
        """
        Initialize the Config object.

        Args:
            **kwargs: Additional keyword arguments to initialize attributes directly.
        """
        super().__init__()
        self._attributes = {}  # Internal dictionary to store configuration attributes
        self.required_keys = []  # Keywords required in the "keys" dictionary
        self.config_dict = None
        # Flatten the structure by removing the top-level key if it exists
        if 'keys' in kwargs:
            self._attributes.update(kwargs['keys'])
        else:
            self._attributes.update(kwargs)
        self.base_required_params = ['keys', 'type']

    def initialize(self, config_dict, name):
        """
        Initialize the configuration with a dictionary and a name.
        """
        if self.required_keys is None:
            raise NotImplementedError("Must implement required keys for config")
        self.name = name
        self.config_dict = config_dict
        self.validate_config()
        self.from_dict(self.config_dict)
        self.check_required_params()

    def validate_config(self):
        """
        Validates that the YAML configuration only contains the allowed top-level keys.

        :param config: The parsed YAML configuration (dict).
        :return: None. Raises ValueError if validation fails.
        """
        allowed_top_keys = {'keys', 'type'}  # Define allowed top-level keys

        # Check for unexpected top-level keys
        for key in self.config_dict:
            if key not in allowed_top_keys:
                raise ValueError(f"Unexpected top-level key: '{key}'")

        # Ensure 'params' is a dictionary
        if 'keys' in self.config_dict and not isinstance(self.config_dict['keys'], dict):
            raise ValueError("'keys' must be a dictionary")

        # Ensure 'type' is a string
        if 'type' in self.config_dict and not isinstance(self.config_dict['type'], str):
            raise ValueError("'type' must be a string")



    def check_required_params(self):
        """
        Validate that all required keywords are present in the "params" dictionary.
        Raises an error if any required parameter is missing.
        """
        keys = list(self._attributes.keys())
        missing_keys = [key for key in self.required_keys if key not in keys]
        if missing_keys:
            raise ValueError(f"Missing required parameters in 'keys': {', '.join(missing_keys)}")

    def set(self, key, value):
        """Set a configuration attribute."""
        self._attributes[key] = value

    def get(self, key, default=None):
        """Get a configuration attribute. Returns `default` if the key is not found."""
        return self._attributes.get(key, default)

    def check(self, key, raise_error=False):
        """
        Check if a given attribute exists and is not None.

        Args:
            key (str): The attribute key to check.
            raise_error (bool): If True, raise a KeyError if the attribute is missing or None.

        Returns:
            bool: True if the attribute exists and is not None, False otherwise.
        """
        if key in self._attributes and self._attributes[key] is not None:
            return True
        if raise_error:
            if key not in self._attributes:
                raise KeyError(f"Attribute '{key}' is missing from the configuration.")
            raise ValueError(f"Attribute '{key}' is set to None in the configuration.")
        return False

    def from_dict(self, input_dict):
        """
        Load configuration attributes from a dictionary.

        Args:
            input_dict (dict): Dictionary of attributes to load into the configuration.
        """
        if not isinstance(input_dict, dict):
            raise ValueError("Input must be a dictionary.")
        # Flatten the structure by removing the top-level key if it exists
        if 'keys' in input_dict:
            self._attributes.update(input_dict['keys'])
        else:
            self._attributes.update(input_dict)

    def to_dict(self):
        """
        Convert the configuration to a dictionary.

        Returns:
            dict: A dictionary representation of the configuration.
        """
        return self._attributes.copy()

    def __getitem__(self, key):
        """Allow dictionary-like access to attributes."""
        return self.get(key)

    def __setitem__(self, key, value):
        """Allow dictionary-like setting of attributes."""
        self.set(key, value)

    def __repr__(self):
        """Provide a string representation of the config attributes."""
        return f"{self.__class__.__name__}({self._attributes})"
