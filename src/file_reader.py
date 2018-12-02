import binascii


class FileReader(object):

    def __init__(self, path):
        self.f = open(path, 'rb')

    def read(self, num_bytes: int) -> int:
        hex_as_str = "".join([self.read1_as_str() for _ in range(num_bytes)][::-1])
        return int(hex_as_str, 16)

    def read_short(self) -> int:
        return self.read(2)

    def read_int(self) -> int:
        return self.read(4)

    def read_char(self) -> str:
        return chr(self.read(2))

    def read_as_hex(self, num_bytes: int) -> hex:
        return hex(self.read(num_bytes))

    def read1_as_str(self) -> str:
        byte = self.f.read(1)
        return binascii.hexlify(byte).decode('utf-8')

    def seek(self, position: int):
        self.f.seek(position)

    def tell(self) -> int:
        return self.f.tell()


if __name__ == "__main__":
    reader = FileReader("extracted/AndroidManifest.xml")
    print(reader.read_short())
    print(reader.read_short(2))
    print(reader.read_as_hex(4))
