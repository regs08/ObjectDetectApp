from datetime import datetime
from model_logic.base_classes.postprocessor import PostprocessorBase
import numpy as np
import supervision as sv

class YOLOPostprocessor(PostprocessorBase):
    def __init__(self, class_labels=None, conf_threshold=0.2):
        """
        Initialize the PostProcessor with class labels and a confidence threshold.
        :param class_labels: List of class labels or None if using a file to load labels.
        :param conf_threshold: Confidence threshold for filtering predictions.
        """
        super().__init__(class_labels, conf_threshold)
        self.class_labels = class_labels
        self.conf_threshold = conf_threshold

    def load_class_labels(self, source):
        """
        Load class labels from a file or directly from a list.
        :param source: Either a path to a .txt file or a list of class labels.
        :return: List of class labels.
        """
        if isinstance(source, str):  # If a file path is provided
            if not source.endswith(".txt"):
                raise ValueError("Unsupported file format. Only .txt files are supported.")
            with open(source, "r") as f:
                class_labels = [line.strip() for line in f.readlines()]
        elif isinstance(source, list):  # If a list of labels is provided directly
            class_labels = source
        else:
            raise ValueError("Source must be a file path (str) or a list of labels.")

        self.class_labels = class_labels

    def postprocess(self, output_data, original_dims) -> sv.Detections:
        """
        Process the model's raw output into human-readable predictions with bounding boxes.
        :param output_data: data from model
        :param original_dims: org dims of image
        :return: sv.detections, returns empty detections if no detections are found
        """
        if not self.class_labels:
            raise ValueError("Class labels are not initialized. Please provide or load class labels.")
        output_tensor = output_data[0]
        detections = {
            'bboxes': [],
            'labels': [],
            'class_ids': [],
            'conf': [],
            'timestamp': []
        }
        original_width, original_height = original_dims

        for i in range(output_tensor.shape[1]):
            box = output_tensor[0, i, :4]
            confidence = output_tensor[0, i, 4]
            class_id = int(output_tensor[0, i, 5])

            if confidence > self.conf_threshold:
                self.populate_detections(detections=detections,
                                         original_height=original_height,
                                         original_width=original_width,
                                         class_id=class_id,
                                         box=box,
                                         confidence=confidence)
        #cast detections to numpy
        detections = self.finalize_detections(detections=detections)

        return detections
    @staticmethod
    def normalize_box(box, original_width, original_height):
        """
        Normalize the bounding box coordinates based on the original image dimensions.
        """
        x_min = int(box[0] * original_width)
        y_min = int(box[1] * original_height)
        x_max = int(box[2] * original_width)
        y_max = int(box[3] * original_height)
        return [x_min, y_min, x_max, y_max]

    def populate_detections(self, detections, box, original_width, original_height, class_id, confidence):
        """
        Populate the detections dictionary with normalized bounding box and other details.
        """
        # Normalize the bounding box
        normalized_box = self.normalize_box(box, original_width, original_height)

        # Add detection details to the dictionary
        detections['bboxes'].append(normalized_box)
        detections['labels'].append(self.class_labels[class_id])
        detections['class_ids'].append(class_id)
        detections['conf'].append(confidence)
        detections['timestamp'].append(datetime.now().isoformat())

        return detections
    @staticmethod
    def finalize_detections(detections):
        """
        Cast lists in the detections dictionary to numpy arrays and converts to SV detecions
        returns empty detections if no detections are found.
        """
        if detections['bboxes']:
            detections['bboxes'] = np.array(detections['bboxes'])
            detections['class_ids'] = np.array(detections['class_ids'])
            detections['conf'] = np.array(detections['conf'])
            # Note labels are added in the detections object during post processing
            sv_detections = sv.Detections(xyxy=detections['bboxes'],
                                          class_id=detections['class_ids'],
                                          confidence=detections['conf'],
                                          metadata={'labels': detections['labels'],
                                                    'timestamp': detections['timestamp']},)
            return sv_detections
        else:
            return sv.Detections.empty()


