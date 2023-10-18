def from_pubkey(cls, pubkey, compressed=True, version=56, prefix=None):
        # Ensure this is a public key
        pubkey = PublicKey(pubkey, prefix=prefix or Prefix.prefix)
        if compressed:
            pubkey_plain = pubkey.compressed()
        else:
            pubkey_plain = pubkey.uncompressed()

        """ Derive address using ``RIPEMD160(SHA512(x))`` """
        addressbin = ripemd160(hashlib.sha512(unhexlify(pubkey_plain)).hexdigest())
        result = Base58(hexlify(addressbin).decode("ascii"))
        return cls(result, prefix=pubkey.prefix)