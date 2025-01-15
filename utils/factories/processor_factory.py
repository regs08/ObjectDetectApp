from model_logic.yolo.postprocessing.yolo_ncnn_postprocessor import YoloNcnnPostprocessor
from model_logic.yolo.preprocessing.yolo_ncnn_preprocessor import YoloNcnnPreprocessor


class ProcessorFactory:
    def __init__(self):
        self.processors = {
            "YoloNcnnPreprocessor" : YoloNcnnPreprocessor,
            "YoloNcnnPostprocessor": YoloNcnnPostprocessor,
        }