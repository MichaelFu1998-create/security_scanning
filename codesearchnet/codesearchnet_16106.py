def decrypt(self, data, ttl=None):
        """
        :type data: bytes
        :type ttl: int
        :rtype: bytes
        """
        data = self._signer.unsign(data, ttl)

        iv = data[:16]
        ciphertext = data[16:]
        decryptor = Cipher(
            algorithms.AES(self._encryption_key), modes.CBC(iv),
            self._backend).decryptor()
        plaintext_padded = decryptor.update(ciphertext)
        try:
            plaintext_padded += decryptor.finalize()
        except ValueError:
            raise InvalidToken

        # Remove padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        unpadded = unpadder.update(plaintext_padded)
        try:
            unpadded += unpadder.finalize()
        except ValueError:
            raise InvalidToken
        return unpadded