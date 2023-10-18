def decode_memo(priv, pub, nonce, message):
    """ Decode a message with a shared secret between Alice and Bob

        :param PrivateKey priv: Private Key (of Bob)
        :param PublicKey pub: Public Key (of Alice)
        :param int nonce: Nonce used for Encryption
        :param bytes message: Encrypted Memo message
        :return: Decrypted message
        :rtype: str
        :raise ValueError: if message cannot be decoded as valid UTF-8
               string

    """
    shared_secret = get_shared_secret(priv, pub)
    aes = init_aes(shared_secret, nonce)
    " Encryption "
    raw = bytes(message, "ascii")
    cleartext = aes.decrypt(unhexlify(raw))
    " Checksum "
    checksum = cleartext[0:4]
    message = cleartext[4:]
    message = _unpad(message, 16)
    " Verify checksum "
    check = hashlib.sha256(message).digest()[0:4]
    if check != checksum:  # pragma: no cover
        raise ValueError("checksum verification failure")
    return message.decode("utf8")