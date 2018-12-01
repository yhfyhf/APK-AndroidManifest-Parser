from enum import Enum
from typing import Tuple

from file_reader import FileReader


class ChunkType(Enum):
    RES_NULL_TYPE = 0x0000
    RES_STRING_POOL_TYPE = 0x0001
    RES_TABLE_TYPE = 0x0002
    RES_XML_TYPE = 0x0003

    # Chunk types in RES_XML_TYPE
    RES_XML_FIRST_CHUNK_TYPE = 0x0100
    RES_XML_START_NAMESPACE_TYPE = 0x0100
    RES_XML_END_NAMESPACE_TYPE = 0x0101
    RES_XML_START_ELEMENT_TYPE = 0x0102
    RES_XML_END_ELEMENT_TYPE = 0x0103
    RES_XML_CDATA_TYPE = 0x0104
    RES_XML_LAST_CHUNK_TYPE = 0x017f
    RES_XML_RESOURCE_MAP_TYPE = 0x0180

    # types in RES_TABLE_TYPE
    RES_TABLE_PACKAGE_TYPE = 0x0200
    RES_TABLE_TYPE_TYPE = 0x0201
    RES_TABLE_TYPE_SPEC_TYPE = 0x0202


class ChunkReader(object):

    def __init__(self, path):
        self._file_reader = FileReader(path)

    def read_chunk_metadata(self) -> Tuple[int, int, int]:
        """
        Chunk Header
            - chunk type: 2 bytes
            - chunk header size: 2 bytes
            - chunk size: (chunk header size - 4) bytes
        """
        chunk_type = self._file_reader.read(2)
        header_size = self._file_reader.read(2)
        remaining_header_size = header_size - 4
        chunk_size = self._file_reader.read(remaining_header_size)
        return chunk_type, header_size, chunk_size


if __name__ == "__main__":
    chunk_reader = ChunkReader("extracted/AndroidManifest.xml")
    print(chunk_reader.read_chunk_metadata())
