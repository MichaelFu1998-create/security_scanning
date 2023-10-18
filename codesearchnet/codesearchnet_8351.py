def unlock(self, pwd):
        """ Unlock the wallet database
        """
        if self.store.is_encrypted():
            return self.store.unlock(pwd)