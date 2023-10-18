def getAccountFromPrivateKey(self, wif):
        """ Obtain account name from private key
        """
        pub = self.publickey_from_wif(wif)
        return self.getAccountFromPublicKey(pub)