from abc import abstractmethod
from enum import Enum

from chunk_parsers.abstract_chunk_parser import AbstractChunkParser
from file_reader import FileReader


class ResourceAttr(Enum):
    LABEL_ATTR = 0x01010001
    ICON_ATTR = 0x01010002
    NAME_ATTR = 0x01010003
    PERMISSION_ATTR = 0x01010006
    RESOURCE_ATTR = 0x01010025
    DEBUGGABLE_ATTR = 0x0101000f
    VERSION_CODE_ATTR = 0x0101021b
    VERSION_NAME_ATTR = 0x0101021c
    SCREEN_ORIENTATION_ATTR = 0x0101001e
    MIN_SDK_VERSION_ATTR = 0x0101020c
    MAX_SDK_VERSION_ATTR = 0x01010271
    REQ_TOUCH_SCREEN_ATTR = 0x01010227
    REQ_KEYBOARD_TYPE_ATTR = 0x01010228
    REQ_HARD_KEYBOARD_ATTR = 0x01010229
    REQ_NAVIGATION_ATTR = 0x0101022a
    REQ_FIVE_WAY_NAV_ATTR = 0x01010232
    TARGET_SDK_VERSION_ATTR = 0x01010270
    TEST_ONLY_ATTR = 0x01010272
    ANY_DENSITY_ATTR = 0x0101026c
    GL_ES_VERSION_ATTR = 0x01010281
    SMALL_SCREEN_ATTR = 0x01010284
    NORMAL_SCREEN_ATTR = 0x01010285
    LARGE_SCREEN_ATTR = 0x01010286
    XLARGE_SCREEN_ATTR = 0x010102bf
    REQUIRED_ATTR = 0x0101028e
    SCREEN_SIZE_ATTR = 0x010102ca
    SCREEN_DENSITY_ATTR = 0x010102cb
    REQUIRES_SMALLEST_WIDTH_DP_ATTR = 0x01010364
    COMPATIBLE_WIDTH_LIMIT_DP_ATTR = 0x01010365
    LARGEST_WIDTH_LIMIT_DP_ATTR = 0x01010366
    PUBLIC_KEY_ATTR = 0x010103a6
    CATEGORY_ATTR = 0x010103e8

    @staticmethod
    def get_name(value: int) -> str:
        try:
            return ResourceAttr(value).name
        except ValueError:
            return "Unknown " + hex(value)


class ResourceMapChunkParser(AbstractChunkParser):
    """
    Header: 8 bytes
        - chunk type: 2 bytes
        - chunk header size: 2 bytes
        - chunk size: 4 bytes
    Body: (chunk size - 8) bytes
        - list of 4 bytes, list of resource attribute ids
    """

    def __init__(self, file_reader: FileReader):
        super().__init__(file_reader)
        self.chunk_type = "Resource Map Chunk"

    @abstractmethod
    def read_header(self):
        pass

    @abstractmethod
    def read_body(self):
        body_size = self.chunk_size - 8
        self.resource_attrs = [ResourceAttr.get_name(self.file_reader.read_int()) for _ in range(int(body_size / 4))]

    def __str__(self):
        return super(ResourceMapChunkParser, self).__str__() + \
               """
            Resource attrs: %s
        """ % (self.resource_attrs)
