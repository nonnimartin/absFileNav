from django.http import HttpResponse

from .chunked_settings import ENCODER, CONTENT_TYPE


class Response(HttpResponse):
    """
    """

    def __init__(self, content, status=None, *args, **kwargs):
        super(Response, self).__init__(
            content=ENCODER(content),
            content_type=CONTENT_TYPE,
            status=status,
            *args, **kwargs
        )
