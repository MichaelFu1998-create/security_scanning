def getAccounts(self):
        """ Return all accounts installed in the wallet database
        """
        pubkeys = self.getPublicKeys()
        accounts = []
        for pubkey in pubkeys:
            # Filter those keys not for our network
            if pubkey[: len(self.prefix)] == self.prefix:
                accounts.extend(self.getAccountsFromPublicKey(pubkey))
        return accounts