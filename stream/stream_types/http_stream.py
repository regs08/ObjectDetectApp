from stream.stream_types.stream_base import Stream

class HTTPStream(Stream):
    """Stream from an HTTP or RTSP source."""
    def __init__(self, url):
        super().__init__(url)
