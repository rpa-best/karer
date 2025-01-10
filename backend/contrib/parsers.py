from rest_framework.parsers import MultiPartParser


class CustomMultiPartParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        data = super(CustomMultiPartParser, self).parse(stream, media_type, parser_context)
        data.data._mutable = True
        data.files._mutable = True
        return data
