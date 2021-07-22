class file_model:
    FullPath: str = None
    ChunkAddress: int = None

    def __init__(self, path: str):
        self.FullPath = path

    def __init__(self, path: str, address: int):
        self.FullPath = path
        self.ChunkAddress = address
