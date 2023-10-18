def getPrivateKeyForPublicKey(self, pub):
        """ Obtain the private key for a given public key

            :param str pub: Public Key
        """
        if str(pub) not in self.store:
            raise KeyNotFound
        return self.store.getPrivateKeyForPublicKey(str(pub))