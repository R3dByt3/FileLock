from Model.filemodel import file_model
from Encryption.key_generator import key_generator
from IO.FileAccess import file_access
from Model.chunk import *


class encrypter():

    __key_gen = key_generator()
    __mask = 0b11111111
    __passwordHash: bytearray = None
    __fileAccess: file_access = None

    def __init__(self, filePath: str, password: str):
        self.__passwordHash = self.__key_gen.get_password_hash(password)
        self.__fileAccess = file_access(filePath, self.__passwordHash)

    def read_files(self) -> list[file_model]:
        return self.__fileAccess.read_files()

    def encrypt2(self, fileModel: file_model) -> None:
        data = self.__fileAccess.read_bytes(fileModel.FullPath)

        fileModel.EncryptionType = 2
        fileModel.Length = len(data)

        crypted = bytearray(self.__passwordHash)

        for count in range(0, len(data)):
            index = count % 128

            if index == 0:
                curr_rnd_hash = self.__key_gen.get_random_hash()

            crypted_byte = (data[count] + curr_rnd_hash[index] +
                            self.__passwordHash[index]) & self.__mask

            crypted.append(curr_rnd_hash[index])
            crypted.append(crypted_byte)

        chunks = list(chunk.get_chunks_for_data(chunk_type.Data, crypted))
        self.__fileAccess.insert_chunks(chunks)

        fileModel.ChunkAddress = chunks[0].ChunkAddress

        self.__fileAccess.write_files([fileModel])

    def decrypt2(self, fileModel: file_model) -> bytearray():
        if fileModel.EncryptionType != 2:
            raise AttributeError
        
        retval = bytearray()
        index = 0

        chunk = self.__fileAccess.get_chunk(fileModel.ChunkAddress)
        current = chunk
        data = bytearray(chunk.Data)

        while (current.NextChunk != None):
            current = current.NextChunk
            data += current.Data
            
        data = data[:fileModel.Length]

        for count in range(0, 127):
            if (data[count] != self.__passwordHash[count]):
                raise PermissionError("Wrong password")

        for count in range(128, len(data), 2):
            hash_byte = data[count]
            crypted_byte = data[count + 1]

            decrypted_byte = (crypted_byte - hash_byte -
                              self.__passwordHash[index]) & self.__mask

            index = index + 1
            index = index % 128

            retval += decrypted_byte

        return retval

    def encrypt(self, fileModel: file_model):
        data = self.__fileAccess.read_bytes(fileModel.FullPath)

        fileModel.EncryptionType = 1
        fileModel.Length = len(data)

        curr_rnd_hash = self.__key_gen.get_random_hash()

        crypted = bytearray(self.__passwordHash)
        crypted += curr_rnd_hash

        for count in range(0, len(data)):
            index = count % 128

            crypted_byte = (data[count] + curr_rnd_hash[index] +
                            self.__passwordHash[index]) & self.__mask

            crypted.append(crypted_byte)

        chunks = list(chunk.get_chunks_for_data(chunk_type.Data, crypted))
        self.__fileAccess.insert_chunks(chunks)

        fileModel.ChunkAddress = chunks[0].ChunkAddress

        self.__fileAccess.write_files([fileModel])

    def decrypt(self, fileModel: file_model) -> bytearray():
        if fileModel.EncryptionType != 1:
            raise AttributeError

        retval = bytearray()
        index = 0

        chunk = self.__fileAccess.get_chunk(fileModel.ChunkAddress)
        current = chunk
        data = bytearray(chunk.Data)

        while (current.NextChunk != None):
            current = current.NextChunk
            data += current.Data

        data = data[:fileModel.Length]

        for count in range(0, len(data), 2):
            hash_byte = data[count]
            crypted_byte = data[count + 1]

            decrypted_byte = (crypted_byte - hash_byte -
                              self.__passwordHash[index]) & self.__mask

            index = index + 1
            index = index % 128

            retval += decrypted_byte

        return retval
