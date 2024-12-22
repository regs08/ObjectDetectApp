from model_logic.yolo.manager.yolo_model_manager import YoloModelManager


class ModelManagerFactory:
    @staticmethod
    def create_model_manager(manager_type: str,):
        """
        Create a model manager based on the type.

        Args:
            manager_type (str): The type of model manager (e.g., "YoloModelManager").
            config_path (str): Path to the configuration file for the model manager.

        Returns:
            BaseModelManager: An instance of the specified model manager.
        """
        if manager_type == "YoloModelManager":
            return YoloModelManager()

        else:
            raise ValueError(f"Unsupported model manager type: {manager_type}")
