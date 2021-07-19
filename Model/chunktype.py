from enum import Enum


class chunk_type(Enum):
    Undefined = 0,
    Header = 1,
    Map = 2,
    Data = 3
