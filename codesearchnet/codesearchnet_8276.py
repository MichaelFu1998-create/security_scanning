def _new_masterpassword(self, password):
        """ Generate a new random masterkey, encrypt it with the password and
            store it in the store.

            :param str password: Password to use for en-/de-cryption
        """
        # make sure to not overwrite an existing key
        if self.config_key in self.config and self.config[self.config_key]:
            raise Exception("Storage already has a masterpassword!")

        self.decrypted_master = hexlify(os.urandom(32)).decode("ascii")

        # Encrypt and save master
        self.password = password
        self._save_encrypted_masterpassword()
        return self.masterkey