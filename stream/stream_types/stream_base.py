import cv2
import os

class Stream:
    def __init__(self, source):
        """
        Base class for all streams or static images.
        :param source: The source of the stream (e.g., file path, URL, camera index, or image file).
        """
        self.source = source
        self.cap = None
        self.is_image = False
        self.image_frame = None
        self.is_opened = True

    def open(self):
        """Open the video stream or load the image."""
        # Check if the source is a video file, camera, or URL
        if isinstance(self.source, int) or self.source.startswith(("http://", "https://")) or self.source.endswith(
                (".mp4", ".avi", ".mkv")):
            self.cap = cv2.VideoCapture(self.source)
            if not self.cap.isOpened():
                raise ValueError(f"Unable to open video stream or file: {self.source}")
        elif os.path.isfile(self.source):
            # Single image file
            self.is_image = True
            self.image_frame = cv2.imread(self.source)
            if self.image_frame is None:
                raise ValueError(f"Unable to load image: {self.source}")
        else:
            raise ValueError(f"Invalid source type: {self.source}")
    def read_frame(self):
        """
        Read a frame from the video stream or return the single image.
        :return: A frame from the stream or the loaded image.
        """
        if self.is_image:
            return self.image_frame  # Return the static image
        if self.cap is None:
            raise RuntimeError("Stream is not open. Call `open()` first.")
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def close(self):
        """Close the video stream."""
        if self.cap:
            self.cap.release()
            self.cap = None
