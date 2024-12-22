from stream.stream_types.stream_base import Stream

class FileStream(Stream):
    """Stream from a local video file."""
    def __init__(self, file_path):
        super().__init__(file_path)
