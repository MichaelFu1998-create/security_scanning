def derive_from_seed(self, offset):
        """ Derive private key using "generate_from_seed" method.
            Here, the key itself serves as a `seed`, and `offset`
            is expected to be a sha256 digest.
        """
        seed = int(hexlify(bytes(self)).decode("ascii"), 16)
        z = int(hexlify(offset).decode("ascii"), 16)
        order = ecdsa.SECP256k1.order
        secexp = (seed + z) % order
        secret = "%0x" % secexp
        if len(secret) < 64: # left-pad with zeroes
            secret = ("0" * (64-len(secret))) + secret
        return PrivateKey(secret, prefix=self.pubkey.prefix)