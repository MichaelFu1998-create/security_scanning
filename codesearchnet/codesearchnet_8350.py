def setKeys(self, loadkeys):
        """ This method is strictly only for in memory keys that are
            passed to Wallet with the ``keys`` argument
        """
        log.debug("Force setting of private keys. Not using the wallet database!")
        if isinstance(loadkeys, dict):
            loadkeys = list(loadkeys.values())
        elif not isinstance(loadkeys, (list, set)):
            loadkeys = [loadkeys]
        for wif in loadkeys:
            pub = self.publickey_from_wif(wif)
            self.store.add(str(wif), pub)