def addPrivateKey(self, wif):
        """ Add a private key to the wallet database
        """
        try:
            pub = self.publickey_from_wif(wif)
        except Exception:
            raise InvalidWifError("Invalid Key format!")
        if str(pub) in self.store:
            raise KeyAlreadyInStoreException("Key already in the store")
        self.store.add(str(wif), str(pub))