from abc import abstractmethod

from chunk_parsers.abstract_chunk_parser import AbstractChunkParser
from file_reader import FileReader


class XMLChunkParser(AbstractChunkParser):
    """
    Header: 8 bytes
        - chunk type: 2 bytes
        - chunk header size: 2 bytes
        - chunk size: 4 bytes
    """

    def __init__(self, file_reader: FileReader):
        super().__init__(file_reader)
        self.chunk_type = "XML Chunk"
        self.read_chunk_header()
        self.read_body()

    @abstractmethod
    def read_chunk_header(self):
        if self.header_size != 8:
            raise Exception("XML Chunk size is " + str(self.header_size) + " instead of 8")

    @abstractmethod
    def read_body(self):
        """ XML chunk has nothing but just the header. """
        pass
