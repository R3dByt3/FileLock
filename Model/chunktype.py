from enum import IntEnum


class chunk_type(IntEnum):
    Undefined = 0,
    Header = 1,
    Map = 2,
    Data = 3
