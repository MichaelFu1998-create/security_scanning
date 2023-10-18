def get_blind_private(self):
        """ Derive private key from the brain key (and no sequence number)
        """
        a = _bytes(self.brainkey)
        return PrivateKey(hashlib.sha256(a).hexdigest(), prefix=self.prefix)