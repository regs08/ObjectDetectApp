from model_logic.yolo.model.yolo_ncnn_model import YoloNcnnModel


model = YoloNcnnModel()
config_file = "/assets/old_configs/ultralytics_config.json"
#model.initialize(config_file)
model._populate_with_config(config_file)
