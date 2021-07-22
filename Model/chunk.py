from Model.chunktype import chunk_type


class chunk():

    __type = chunk_type.Undefined
    Data = bytearray(1024 * 1024)
    ChunkAddress = -1
    NextChunkAddress = -1
    NextChunk: 'chunk' = None

    def __init__(self, chunk_type: chunk_type, data: bytearray):

        for x in range(0, 1024 * 1024 + 8 - len(data)):
            data.append(0)

        self.Type = chunk_type
        self.Data = data

    def serialize(self) -> bytearray:

        data = bytearray(int(self.__type).to_bytes(2, "big"))
        data += self.Data
        data += bytearray(self.NextChunkAddress.to_bytes(2,
                          byteorder="big", signed=True))
        return data

    def deserialize(self, data: bytearray):

        self.__type = chunk_type(int.from_bytes(data[:4], "big"))
        self.Data = data[4:1024*1024 + 4]
        self.NextChunkAddress = int.from_bytes(
            data[1024*1024 + 4:], byteorder="big", signed=True)

    @staticmethod
    def get_chunks_for_data(chunk_type: chunk_type, data: bytearray) -> list['chunk']:

        last_chunk: chunk = None
        current_chunk: chunk = None

        for index in range(0, len(data), 1024 * 1024):
            current_chunk = chunk(chunk_type, data[index:index + 1024 * 1024])

            if (last_chunk != None):
                last_chunk.NextChunk = current_chunk

            yield current_chunk

            last_chunk = current_chunk
