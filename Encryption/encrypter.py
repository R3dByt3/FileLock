from Encryption.key_generator import key_generator


class encrypter():

    __key_gen = key_generator()
    __mask = 0b11111111

    def encrypt2(self, data: bytearray, password: str):

        password_hash = self.__key_gen.get_password_hash(password)
        retval = bytearray(password_hash)

        for count in range(0, len(data)):
            index = count % 128

            if index == 0:
                curr_rnd_hash = self.__key_gen.get_random_hash()

            crypted_byte = (data[count] + curr_rnd_hash[index] +
                            password_hash[index]) & self.__mask

            retval.append(curr_rnd_hash[index])
            retval.append(crypted_byte)

        return retval

    def decrypt2(self, data: bytearray, password: str):

        password_hash = self.__key_gen.get_password_hash(password)
        retval = bytearray()
        index = 0

        for count in range(0, 127):
            if (data[count] != password_hash[count]):
                raise PermissionError("Wrong password")

        for count in range(128, len(data), 2):
            hash_byte = data[count]
            crypted_byte = data[count + 1]

            decrypted_byte = (crypted_byte - hash_byte -
                              password_hash[index]) & self.__mask

            index = index + 1
            index = index % 128

            retval.append(decrypted_byte)

        return retval

    def encrypt(self, data: bytearray, password: str):

        password_hash = self.__key_gen.get_password_hash(password)
        curr_rnd_hash = self.__key_gen.get_random_hash()

        retval = bytearray(password_hash)
        retval.append(curr_rnd_hash)

        for count in range(0, len(data)):
            index = count % 128

            crypted_byte = (data[count] + curr_rnd_hash[index] +
                            password_hash[index]) & self.__mask

            retval.append(crypted_byte)

        return retval

    def decrypt(self, data: bytearray, password: str):

        password_hash = self.__key_gen.get_password_hash(password)
        retval = bytearray()
        index = 0

        for count in range(0, len(data), 2):
            hash_byte = data[count]
            crypted_byte = data[count + 1]

            decrypted_byte = (crypted_byte - hash_byte -
                              password_hash[index]) & self.__mask

            index = index + 1
            index = index % 128

            retval.append(decrypted_byte)

        return retval
