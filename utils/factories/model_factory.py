from model_logic.yolo.model.yolo_model import YOLOModel
from model_logic.yolo.model.yolo_ncnn_model import YoloNcnnModel

class ModelFactory:
    def __init__(self):
        self.models ={
            'YoloModel': YOLOModel,
            'YoloNCNNModel': YoloNcnnModel,
        }