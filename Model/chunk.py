from Model.chunktype import chunk_type


class chunk():

    Type = chunk_type.Undefined
    Data = bytearray(1024 * 1024)
    ChunkAddress = -1
    NextChunkAddress = -1
    NextChunk: 'chunk' = None

    def __init__(self, chunk_type: chunk_type, data: bytearray):

        data += bytearray(1024 * 1024 - len(data))

        self.Type = chunk_type
        self.Data = data

    def serialize(self) -> bytearray:

        data = bytearray(int(self.Type).to_bytes(2, "big"))
        data += self.Data
        data += bytearray(self.NextChunkAddress.to_bytes(2,
                          byteorder="big", signed=True))
        return data

    def deserialize(self, data: bytearray):

        self.Type = chunk_type(int.from_bytes(data[:2], "big"))
        self.Data = data[2:1024*1024 + 2]
        self.NextChunkAddress = int.from_bytes(
            data[1024*1024 + 2:], byteorder="big", signed=True)

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
