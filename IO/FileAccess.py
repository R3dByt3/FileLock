def read_bytes(filePath: str):
    if not isinstance(filePath, str):
        raise ValueError("filePath has to be of type string")

    bytes = bytearray()
    with open(filePath, "rb") as f:
        while (byte := f.read(1)):
            bytes.append(byte)

    return bytes


def write_bytes(filePath: str, data: bytearray):
    if not isinstance(filePath, str):
        raise ValueError("filePath has to be of type string")

    if not isinstance(data, (bytes, bytearray)):
        raise ValueError("data has to be of type byte array")

    with open(filePath, "w") as f:
        f.write(data)
