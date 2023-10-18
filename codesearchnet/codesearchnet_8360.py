def getAccountsFromPublicKey(self, pub):
        """ Obtain all accounts associated with a public key
        """
        names = self.rpc.get_key_references([str(pub)])[0]
        for name in names:
            yield name