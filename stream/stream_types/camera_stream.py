from stream.stream_types.stream_base import Stream

class CameraStream(Stream):
    """Stream from a local camera."""
    def __init__(self, camera_index=0):
        super().__init__(camera_index)

