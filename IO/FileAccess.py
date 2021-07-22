from Projekt.Model.filemodel import file_model
from Projekt.Model.chunk import chunk
from Projekt.Model.chunktype import chunk_type


class file_access:

    __filePath: str = None
    __passwordHash: bytearray = None

    def __init__(self, filePath: str, passwordHash: bytearray):
        self.__filePath = filePath
        self.__passwordHash = passwordHash

        chunks = self.read_chunks(chunk_type.Header)
        firstHeader = next(
            obj for obj in chunks if obj.Type == chunk_type.Header)

        for index in range(0, 128):
            if passwordHash[index] != firstHeader.Data[index]:
                raise PermissionError("Password is incorrect")

    def read_files(self) -> list[file_model]:
        chunks = self.read_chunks(chunk_type.Map)

        for single in chunks:
            current = single
            data = bytearray(current.Data)
            while (single.NextChunk != None):
                current = current.NextChunk
                data.append(current.Data)

            content = data.decode("UTF-8")

        parts = content.split("*/")

        for index in range(0, len(parts), 2):
            yield file_model(parts[index], parts[index + 1])

    def write_all_chunks(self, chunks: list[chunk]):
        with open(self.__filePath, "wb") as f:
            for index in range(0, len(chunks)):
                f.write(chunks[index].serialize())

    def update_chunks(self, chunks: list[chunk]):
        with open(self.__filePath, "wb") as f:
            for index in range(0, len(chunks)):
                f.seek(chunks[index].Index * 1024 * 1024 + 8)
                f.write(chunks[index].serialize())

    def read_chunks(self, searchType: chunk_type) -> list[chunk]:

        chunks: list[chunk] = []
        retVal: list[chunk] = []

        with open(self.__filePath, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(0)

            current: chunk = None
            address = 0

            while(f.tell() < size):
                type = chunk_type(int.from_bytes(f.read(4)))
                data = f.read(1024 * 1024)

                if type == searchType:
                    current = chunk(data)
                    current.NextChunkAddress = int.from_bytes(
                        f.read(4))
                else:
                    f.seek(1024 * 1024 + 4)

                current.ChunkAddress = address
                address = address + 1024 * 1024 + 8

                chunks.append(current)

        for single in chunks.copy():
            retVal.append(self.resolve_childs(single, chunks))

        return retVal

    def resolve_childs(self, single: chunk, chunks: list[chunk]) -> chunk:
        if (single.NextChunkAddress != 0):
            single.NextChunk = next(
                obj for obj in chunks if obj.ChunkAddress == single.NextChunkAddress)
            chunks.remove(single.NextChunk)

        return single
