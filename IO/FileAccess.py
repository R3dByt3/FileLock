from io import SEEK_END
from Model.filemodel import file_model
from Model.chunk import chunk
from Model.chunktype import chunk_type
import os.path
import os


class file_access:

    __filePath: str = None
    __passwordHash: bytearray = None

    def __init__(self, filePath: str, passwordHash: bytearray):
        self.__filePath = filePath
        self.__passwordHash = passwordHash

        if os.path.isfile(filePath):
            chunks = list(self.read_chunks(chunk_type.Header))
            firstHeader = next(
                obj for obj in chunks if obj.Type == chunk_type.Header)

            for index in range(0, 128):
                if passwordHash[index] != firstHeader.Data[index]:
                    raise PermissionError("Password is incorrect")

        else:
            headers = list(chunk.get_chunks_for_data(
                chunk_type.Header, passwordHash))
            self.insert_chunks(headers)

    def read_bytes(self, filePath: str) -> bytearray:
        bytes = bytearray()
        with open(filePath, "rb") as f:
            bytes = f.read()

        return bytes

    def write_bytes(self, filePath: str, data: bytearray):
        with open(filePath, "wb") as f:
            f.write(data)

    def get_chunk(self, findAddress: int) -> chunk:
        with open(self.__filePath, "rb") as f:
            f.seek(findAddress)

            current: chunk = None
            type = chunk_type(int.from_bytes(f.read(2), "big"))

            data = bytearray(f.read(1024 * 1024))
            current = chunk(type, data)
            current.NextChunkAddress = int.from_bytes(
                f.read(2), byteorder="big", signed=True)
            current.ChunkAddress = findAddress
        
        if current.NextChunkAddress != -1:
            current.NextChunk = self.get_chunk(current.NextChunkAddress)

    def write_files(self, files: list[file_model]):
        content = ''.join(
            [num.FullPath + "*/" + str(num.ChunkAddress) for num in files])

        data = bytearray(content.encode("UTF-8"))

        chunks = list(chunk.get_chunks_for_data(chunk_type.Map, data))
        self.insert_chunks(chunks)

    def read_files(self) -> list[file_model]:
        chunks = self.read_chunks(chunk_type.Map)

        content = None

        for single in chunks:
            current = single
            data = bytearray(current.Data)
            while (single.NextChunk != None):
                current = current.NextChunk
                data += current.Data

            content = data.decode("UTF-8")

        if content == None:
            return list[file_model]

        parts = content.split("*/")

        for index in range(0, len(parts), 2):
            yield file_model(parts[index], parts[index + 1])

    def write_all_chunks(self, chunks: list[chunk]):
        with open(self.__filePath, "wb") as f:
            for index in range(0, len(chunks)):
                f.write(chunks[index].serialize())

    def insert_chunks(self, chunks: list[chunk]):
        with open(self.__filePath, "wb") as f:
            for index in range(0, len(chunks)):
                if chunks[index].ChunkAddress != -1:
                    f.seek(chunks[index].ChunkAddress)
                    f.write(chunks[index].serialize())
                else:
                    f.seek(0, os.SEEK_END)
                    chunks[index].ChunkAddress = f.tell()
                    f.write(chunks[index].serialize())

    def read_chunks(self, searchType: chunk_type) -> list[chunk]:

        chunks: list[chunk] = []
        retVal: list[chunk] = []

        with open(self.__filePath, "rb") as f:
            f.seek(0, 2)
            size = f.tell()
            f.seek(0)

            while(f.tell() < size):
                current: chunk = None
                address = 0
                type = chunk_type(int.from_bytes(f.read(2), "big"))

                if type == searchType:
                    data = bytearray(f.read(1024 * 1024))
                    current = chunk(searchType, data)
                    current.NextChunkAddress = int.from_bytes(
                        f.read(2), byteorder="big", signed=True)
                    current.ChunkAddress = address
                    chunks.append(current)
                else:
                    f.seek(1024 * 1024 + 2, os.SEEK_CUR)

                address = address + 1024 * 1024 + 4

        for single in chunks.copy():
            retVal.append(self.resolve_childs(single, chunks))

        return retVal

    def resolve_childs(self, single: chunk, chunks: list[chunk]) -> chunk:
        if (single.NextChunkAddress != 0):
            single.NextChunk = next(
                obj for obj in chunks if obj.ChunkAddress == single.NextChunkAddress)
            chunks.remove(single.NextChunk)

        return single
