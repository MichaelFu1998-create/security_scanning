def encode_memo(priv, pub, nonce, message):
    """ Encode a message with a shared secret between Alice and Bob

        :param PrivateKey priv: Private Key (of Alice)
        :param PublicKey pub: Public Key (of Bob)
        :param int nonce: Random nonce
        :param str message: Memo message
        :return: Encrypted message
        :rtype: hex

    """
    shared_secret = get_shared_secret(priv, pub)
    aes = init_aes(shared_secret, nonce)
    " Checksum "
    raw = bytes(message, "utf8")
    checksum = hashlib.sha256(raw).digest()
    raw = checksum[0:4] + raw
    " Padding "
    raw = _pad(raw, 16)
    " Encryption "
    return hexlify(aes.encrypt(raw)).decode("ascii")