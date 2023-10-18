def child(self, offset256):
        """ Derive new private key from this key and a sha256 "offset"
        """
        a = bytes(self.pubkey) + offset256
        s = hashlib.sha256(a).digest()
        return self.derive_from_seed(s)