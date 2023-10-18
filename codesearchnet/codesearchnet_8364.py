def getPublicKeys(self, current=False):
        """ Return all installed public keys

            :param bool current: If true, returns only keys for currently
                connected blockchain
        """
        pubkeys = self.store.getPublicKeys()
        if not current:
            return pubkeys
        pubs = []
        for pubkey in pubkeys:
            # Filter those keys not for our network
            if pubkey[: len(self.prefix)] == self.prefix:
                pubs.append(pubkey)
        return pubs