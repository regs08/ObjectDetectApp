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
        self.required_params = []  # Keywords required in the "params" dictionary
        # Flatten the structure by removing the top-level key if it exists
        if 'params' in kwargs:
            self._attributes.update(kwargs['params'])
        else:
            self._attributes.update(kwargs)

    def initialize(self, config_dict, name):
        """
        Initialize the configuration with a dictionary and a name.
        """
        if self.required_params is None:
            raise NotImplementedError("Must implement required params for config")
        self.name = name
        self.from_dict(config_dict)
        self.check_required_params()

    def check_required_params(self):
        """
        Validate that all required keywords are present in the "params" dictionary.
        Raises an error if any required parameter is missing.
        """
        params = list(self._attributes.keys())
        missing_params = [param for param in self.required_params if param not in params]
        if missing_params:
            raise ValueError(f"Missing required parameters in 'params': {', '.join(missing_params)}")

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
        if 'params' in input_dict:
            self._attributes.update(input_dict['params'])
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
