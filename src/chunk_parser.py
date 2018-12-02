from abc import abstractmethod

from file_reader import FileReader


class AbstractChunkReader(object):
    """
    Chunk
        Chunk Header
            - chunk type: 2 bytes
            - chunk header size: 2 bytes
            - chunk size: 4 bytes
            - ...
        Chunk Body
            ...
    """

    def __init__(self, file_reader):
        self.file_reader = file_reader
        self.header_size = self.file_reader.read(2)
        self.chunk_size = self.file_reader.read(4)

    def read_chunk_header(self):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError


class XMLChunkReader(AbstractChunkReader):

    def __init__(self, file_reader):
        super().__init__(file_reader)

    @abstractmethod
    def read_chunk_header(self):
        """
        Chunk Header: 8 bytes
            - chunk type: 2 bytes
            - chunk header size: 2 bytes
            - chunk size: 4 bytes
        """
        if self.header_size != 8:
            raise Exception("XML Chunk size is " + str(self.header_size) + " instead of 8")

    def __str__(self):
        return """Chunk type: XML Chunk Reader
            Chunk header size: %s (%d)
            Chunk size: %s (%d)
        """ % (hex(self.header_size), self.header_size, hex(self.chunk_size), self.chunk_size)


class StringPoolChunkReader(AbstractChunkReader):

    def __init__(self, file_reader: FileReader):
        super().__init__(file_reader)
        self.string_count = None
        self.style_count = None
        self.read_chunk_header()

    @abstractmethod
    def read_chunk_header(self):
        """
        StringPoolChunk Header: 28 bytes
            - chunk type: 2 bytes
            - chunk header size: 2 bytes
            - chunk size: 4 bytes
            - string count: 4 bytes
            - style count: 4 bytes
            - flag: 4 bytes.
                enum {
                    SORTED_FLAG = 1<<0, If set, the string index is sorted by the string values (based on strcmp16()).
                    UTF8_FLAG = 1<<8, String pool is encoded in UTF-8
                }
            - strings start: 4 bytes (Index of the string pool from the chunk header)
            - styles start: 4 bytes (Index of the styles pool from the chunk header)
            - list of 4 bytes, of length string count. Each means index of the string from the string pool
            - list of 4 bytes, of length style count. Each means index of the style from the style pool. If style count is 0, this doesn't exist.
            - string pool (the actual strings, each character takes 2 bytes):
                string length: 2 bytes
                actual string: string length * 2 bytes
                0x0000: 2 bytes (end of each string)
        """
        self.string_count = self.file_reader.read(4)
        self.style_count = self.file_reader.read(4)

    def __str__(self):
        return """Chunk type: String Pool Chunk Reader
            Chunk header size: %s (%d)
            Chunk size: %s (%d)
            String count: %s (%d)
            Style count: %s (%d)
        """ % (hex(self.header_size), self.header_size, hex(self.chunk_size), self.chunk_size, hex(self.string_count),
               self.string_count, hex(self.style_count), self.style_count)
