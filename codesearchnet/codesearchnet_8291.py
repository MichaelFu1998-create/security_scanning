def derive_private_key(self, sequence):
        """ Derive new private key from this private key and an arbitrary
            sequence number
        """
        encoded = "%s %d" % (str(self), sequence)
        a = bytes(encoded, "ascii")
        s = hashlib.sha256(hashlib.sha512(a).digest()).digest()
        return PrivateKey(hexlify(s).decode("ascii"), prefix=self.pubkey.prefix)