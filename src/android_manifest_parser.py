from enum import Enum

from file_reader import FileReader
from chunk_parsers.string_pool_chunk_parser import StringPoolChunkParser
from chunk_parsers.xml_chunk_parser import XMLChunkParser
from chunk_parsers.resource_map_chunk_parser import ResourceMapChunkParser


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


class ManifestReader(object):

    """
    AndroidManifest.xml
        XML Chunk
        String Pool Chunk
        Resource Map Chunk
    """

    def __init__(self, path):
        self.file_reader = FileReader(path)

    def get_chunk_type(self) -> int:
        """
        Chunk Header
            - chunk type: 2 bytes
            - chunk header size: 2 bytes
            - chunk size: 4 bytes
        """
        return self.file_reader.read_short()


if __name__ == "__main__":
    manifest_reader = ManifestReader("extracted/AndroidManifest.xml")

    chunk_type = manifest_reader.get_chunk_type()
    if chunk_type != ChunkType.RES_XML_TYPE.value:
        raise Exception("First chunk should be XML chunk")
    xml_chunk_parser = XMLChunkParser(manifest_reader.file_reader)
    print(xml_chunk_parser)

    chunk_type = manifest_reader.get_chunk_type()
    if chunk_type != ChunkType.RES_STRING_POOL_TYPE.value:
        raise Exception("Second chunk should be string pool chunk")
    string_pool_chunk_parser = StringPoolChunkParser(manifest_reader.file_reader)
    print(string_pool_chunk_parser)

    chunk_type = manifest_reader.get_chunk_type()
    if chunk_type != ChunkType.RES_XML_RESOURCE_MAP_TYPE.value:
        raise Exception("Third chunk should be resource map chunk")
    resource_map_chunk_parser = ResourceMapChunkParser(manifest_reader.file_reader)
    print(resource_map_chunk_parser)
