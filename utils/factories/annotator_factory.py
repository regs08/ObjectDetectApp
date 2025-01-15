from annotator.detections.detections_annotator import FrameAnnotatorDetections

class AnnotatorFactory:
    def __init__(self):
        self.annotators = {'DetectionAnnotator': FrameAnnotatorDetections}