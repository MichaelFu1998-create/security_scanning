def change_password(self, newpassword):
        """ Change the password that allows to decrypt the master key
        """
        if not self.unlocked():
            raise WalletLocked
        self.password = newpassword
        self._save_encrypted_masterpassword()