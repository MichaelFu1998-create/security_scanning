def recoverPubkeyParameter(message, digest, signature, pubkey):
    """ Use to derive a number that allows to easily recover the
        public key from the signature
    """
    if not isinstance(message, bytes):
        message = bytes(message, "utf-8")  # pragma: no cover
    for i in range(0, 4):
        if SECP256K1_MODULE == "secp256k1":  # pragma: no cover
            sig = pubkey.ecdsa_recoverable_deserialize(signature, i)
            p = secp256k1.PublicKey(pubkey.ecdsa_recover(message, sig))
            if p.serialize() == pubkey.serialize():
                return i
        elif SECP256K1_MODULE == "cryptography" and not isinstance(pubkey, PublicKey):
            p = recover_public_key(digest, signature, i, message)
            p_comp = hexlify(compressedPubkey(p))
            pubkey_comp = hexlify(compressedPubkey(pubkey))
            if p_comp == pubkey_comp:
                return i
        else:  # pragma: no cover
            p = recover_public_key(digest, signature, i)
            p_comp = hexlify(compressedPubkey(p))
            p_string = hexlify(p.to_string())
            if isinstance(pubkey, PublicKey):  # pragma: no cover
                pubkey_string = bytes(repr(pubkey), "ascii")
            else:  # pragma: no cover
                pubkey_string = hexlify(pubkey.to_string())
            if p_string == pubkey_string or p_comp == pubkey_string:  # pragma: no cover
                return i