class file_model:
    FullPath: str = None
    ChunkAddress: int = None
    EncryptionType: int = None
    Length: int = None

    def __init__(self, path: str, address: int):
        self.FullPath = path
        self.ChunkAddress = address
        self.EncryptionType = 0
        self.Length = 0
