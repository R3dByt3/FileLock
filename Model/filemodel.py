class file_model:
    __fullPath: str = None
    __chunkAddress: int = None

    def __init__(self, path: str):
        self.__fullPath = path

    def __init__(self, path: str, address: int):
        self.__fullPath = path
        self.__chunkAddress = address
