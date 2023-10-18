def from_privkey(cls, privkey, prefix=None):
        """ Derive uncompressed public key """
        privkey = PrivateKey(privkey, prefix=prefix or Prefix.prefix)
        secret = unhexlify(repr(privkey))
        order = ecdsa.SigningKey.from_string(
            secret, curve=ecdsa.SECP256k1
        ).curve.generator.order()
        p = ecdsa.SigningKey.from_string(
            secret, curve=ecdsa.SECP256k1
        ).verifying_key.pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), order)
        # y_str = ecdsa.util.number_to_string(p.y(), order)
        compressed = hexlify(chr(2 + (p.y() & 1)).encode("ascii") + x_str).decode(
            "ascii"
        )
        # uncompressed = hexlify(
        #    chr(4).encode('ascii') + x_str + y_str).decode('ascii')
        return cls(compressed, prefix=prefix or Prefix.prefix)