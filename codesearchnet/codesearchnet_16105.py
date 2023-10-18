def _encrypt_from_parts(self, data, iv):
        """
        :type data: bytes
        :type iv: bytes
        :rtype: any
        """
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(data) + padder.finalize()
        encryptor = Cipher(
            algorithms.AES(self._encryption_key), modes.CBC(iv),
            self._backend).encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        return self._signer.sign(iv + ciphertext)