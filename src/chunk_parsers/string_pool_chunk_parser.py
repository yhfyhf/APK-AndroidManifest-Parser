from abc import abstractmethod

from chunk_parsers.abstract_chunk_parser import AbstractChunkParser
from file_reader import FileReader


class StringPoolChunkParser(AbstractChunkParser):
    """
    Header: 28 bytes
        - chunk type: 2 bytes
        - chunk header size: 2 bytes
        - chunk size: 4 bytes
        - string count: 4 bytes
        - style count: 4 bytes
        - flag: 4 bytes
            enum {
                SORTED_FLAG = 1<<0, If set, the string index is sorted by the string values (based on strcmp16()).
                UTF8_FLAG = 1<<8, String pool is encoded in UTF-8
            }
        - strings start: 4 bytes (Index of the string pool from the chunk header)
        - styles start: 4 bytes (Index of the styles pool from the chunk header)
    Body
        - list of 4 bytes, of length string count. Each means index of the string from the string pool
        - list of 4 bytes, of length style count. Each means index of the style from the style pool. If style count is 0, this doesn't exist.
        - string pool (the actual strings, each character takes 2 bytes):
            string length: 2 bytes
            actual string: string length * 2 bytes
            0x0000: 2 bytes (end of each string)
    """

    def __init__(self, file_reader: FileReader):
        super().__init__(file_reader)
        self.chunk_type = "String Pool Chunk"

    @abstractmethod
    def read_header(self):
        self.string_count = self.file_reader.read_int()
        self.style_count = self.file_reader.read_int()
        self.flag = self.file_reader.read_int()
        self.strings_start = self.file_reader.read_int()
        self.styles_start = self.file_reader.read_int()

    @abstractmethod
    def read_body(self):
        string_offsets = [self.file_reader.read_int() for _ in range(self.string_count)]
        style_offsets = [self.file_reader.read_int() for _ in range(self.style_count)]
        temp = self.file_reader.tell()
        self.strings = [self.read_a_string(self.chunk_offset + self.strings_start + string_offset) for string_offset in
                        string_offsets]
        self.file_reader.seek(temp)
        # TODO: I have no idea how to read style pool
        self.file_reader.seek(self.chunk_offset + self.chunk_size)

    def read_a_string(self, str_position) -> str:
        self.file_reader.seek(str_position)
        length = self.file_reader.read_short()
        string = "".join([self.file_reader.read_char() for _ in range(length)])
        if self.file_reader.read_char() != '\x00':
            raise Exception("end of string is not \x00")
        return string

    def __str__(self):
        return super(StringPoolChunkParser, self).__str__() +\
        """
            String count: %s (%d)
            Style count: %s (%d)
            Strings: %s
        """ % (hex(self.string_count), self.string_count, hex(self.style_count), self.style_count, self.strings)
