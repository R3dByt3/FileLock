from abc import ABCMeta, abstractmethod
from Projekt.Model.chunktype import chunk_type
from Projekt.Model.header_chunk import header_chunk
from Projekt.Model.chunk import chunk


class chunk(object, metaclass=ABCMeta):

    __type = chunk_type.Undefined
    Data = bytearray(1024 * 1024)
    Index = -1
    ChunkAddress = 0
    NextChunkAddress = 0
    NextChunk = None

    @abstractmethod
    def __init__(self, chunk_type: chunk_type):

        self.Type = chunk_type

    def serialize(self) -> bytearray:

        data = bytearray(self.__type)
        data.append(self.Data)
        data.append(self.NextChunkAddress)
        return data

    def deserialize(self, data: bytearray):

        self.__type = chunk_type(int.from_bytes(data[:4], "big"))
        self.Data = data[4:1024*1024 + 4]
        self.NextChunkAddress = int.from_bytes(data[1024*1024 + 4:], "big")

    @staticmethod
    def get_chunks_for_data(self, chunk_type: chunk_type, data: bytearray) -> list[chunk]:

        last_chunk: chunk = None
        current_chunk: chunk = None

        for index in range(0, len(data), 1024 * 1024):
            if (chunk_type is chunk_type.Header):
                current_chunk = header_chunk(data[index:index + 1024 * 1024])
            elif (chunk_type is chunk_type.Map):
                pass
            elif (chunk_type is chunk_type.Data):
                pass
            else:
                raise NotImplementedError

            if (last_chunk is not None):
                last_chunk.NextChunk = current_chunk

            last_chunk = current_chunk
