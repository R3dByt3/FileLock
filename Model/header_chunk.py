from Scripting.Projekt.Model.__pycache__.chunktype import chunk_type
from Projekt.Encryption.key_generator import key_generator
from Projekt.Model.chunk import chunk


class header_chunk(chunk):

    def __init__(self, data: bytearray):
        super(chunk, self).__init__(chunk_type.Header)
        Data = data
