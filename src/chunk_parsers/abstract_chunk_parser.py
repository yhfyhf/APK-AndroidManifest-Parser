from file_reader import FileReader


class AbstractChunkParser(object):
    """
    Chunk Header
        - chunk type: 2 bytes
        - chunk header size: 2 bytes
        - chunk size: 4 bytes
        - ...
    Chunk Body
        ...
    """

    def __init__(self, file_reader: FileReader):
        self.file_reader = file_reader
        self.chunk_type = "Abstract Chunk"
        self.chunk_offset = file_reader.tell() - 2  # chunk type is already read
        self.header_size = self.file_reader.read_short()
        self.chunk_size = self.file_reader.read_int()
        self.read_header()
        self.read_body()

    def read_header(self):
        raise NotImplementedError

    def read_body(self):
        raise NotImplementedError

    def __str__(self):
        return """Chunk type: %s
            Chunk header size: %s (%d)
            Chunk size: %s (%d)
        """ % (self.chunk_type, hex(self.header_size), self.header_size, hex(self.chunk_size), self.chunk_size)
