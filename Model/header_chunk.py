from Scripting.Projekt.Model.__pycache__.chunktype import chunk_type
from Scripting.Projekt.Encryption.key_generator import key_generator
from chunk import chunk


class header_chunk(chunk):

    def __init__(self, data: bytearray):
        super(chunk_type.Header)
        Data = data
