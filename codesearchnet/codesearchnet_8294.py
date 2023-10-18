def from_pubkey(cls, pubkey, compressed=False, version=56, prefix=None):
        # Ensure this is a public key
        pubkey = PublicKey(pubkey)
        if compressed:
            pubkey = pubkey.compressed()
        else:
            pubkey = pubkey.uncompressed()

        """ Derive address using ``RIPEMD160(SHA256(x))`` """
        addressbin = ripemd160(hexlify(hashlib.sha256(unhexlify(pubkey)).digest()))
        return cls(hexlify(addressbin).decode("ascii"))