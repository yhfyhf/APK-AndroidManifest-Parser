import binascii


class FileReader(object):

    def __init__(self, path):
        self.f = open(path, 'rb')

    def __del__(self):
        self.f.close()

    def read(self, num_bytes) -> int:
        hex_as_str = "".join([self.read1_as_str() for _ in range(num_bytes)][::-1])
        return int(hex_as_str, 16)

    def read_as_hex(self, num_bytes) -> hex:
        hex_as_str = "".join([self.read1_as_str() for _ in range(num_bytes)])[::-1]
        return hex(int(hex_as_str, 16))

    def read1_as_str(self) -> str:
        byte = self.f.read(1)
        return binascii.hexlify(byte).decode('utf-8')


if __name__ == "__main__":
    reader = FileReader("extracted/AndroidManifest.xml")
    print(reader.read(2))
    print(reader.read(2))
    print(reader.read_as_hex(4))
