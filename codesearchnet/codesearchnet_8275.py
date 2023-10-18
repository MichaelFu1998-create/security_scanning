def _decrypt_masterpassword(self):
        """ Decrypt the encrypted masterkey
        """
        aes = AESCipher(self.password)
        checksum, encrypted_master = self.config[self.config_key].split("$")
        try:
            decrypted_master = aes.decrypt(encrypted_master)
        except Exception:
            self._raise_wrongmasterpassexception()
        if checksum != self._derive_checksum(decrypted_master):
            self._raise_wrongmasterpassexception()
        self.decrypted_master = decrypted_master