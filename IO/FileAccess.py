from Projekt.Model.header_chunk import header_chunk
from Projekt.Model.chunk import chunk
from Projekt.Model.chunktype import chunk_type


class file_access:

    __filePath = str()

    def __init__(self, filePath: str):
        self.__filePath = filePath

    def read_bytes(self) -> bytearray:
        bytes = bytearray()
        with open(self.__filePath, "rb") as f:
            while (byte := f.read(1)):
                bytes.append(byte)

        return bytes

    def write_bytes(self, data: bytearray):
        with open(self.__filePath, "wb") as f:
            f.write(data)

    def write_all_chunks(self, chunks: list[chunk]):
        with open(self.__filePath, "wb") as f:
            for index in range(0, len(chunks)):
                f.write(chunks[index].serialize())

    def update_chunks(self, chunks: list[chunk]):
        with open(self.__filePath, "wb") as f:
            for index in range(0, len(chunks)):
                f.seek(chunks[index].Index * 1024 * 1024 + 8)
                f.write(chunks[index].serialize())

    def read_meta_chunks(self) -> list[chunk]:
        with open(self.__filePath, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(0)
            while(f.tell() < size):
                type = chunk_type(int.from_bytes(f.read(4)))

                if type is chunk_type.Header:
                    data = f.read(1024 * 1024)
                    header = header_chunk(data)
                    header.NextChunkAddress = int.from_bytes(
                        f.read(4))  # ToDo: Static Reader impl für single
                    yield
                elif type is chunk_type.Map:
                    pass
                else:
                    f.seek(1024 * 1024 + 4)
