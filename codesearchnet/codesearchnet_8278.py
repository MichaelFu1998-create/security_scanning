def _get_encrypted_masterpassword(self):
        """ Obtain the encrypted masterkey

            .. note:: The encrypted masterkey is checksummed, so that we can
                figure out that a provided password is correct or not. The
                checksum is only 4 bytes long!
        """
        if not self.unlocked():
            raise WalletLocked
        aes = AESCipher(self.password)
        return "{}${}".format(
            self._derive_checksum(self.masterkey), aes.encrypt(self.masterkey)
        )