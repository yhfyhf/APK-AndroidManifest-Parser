from abc import abstractmethod

from chunk_parsers.abstract_chunk_parser import AbstractChunkParser
from file_reader import FileReader


class ResourceMapChunkParser(AbstractChunkParser):
    """
    Header: 28 bytes
        - chunk type: 2 bytes
        - chunk header size: 2 bytes
        - chunk size: 4 bytes
    """

    def __init__(self, file_reader: FileReader):
        super().__init__(file_reader)
        self.read_body()

    @abstractmethod
    def read_header(self):
        pass

    @abstractmethod
    def read_body(self):
        pass
