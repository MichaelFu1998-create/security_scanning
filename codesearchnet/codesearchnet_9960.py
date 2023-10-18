def rc4_decrypt(key, data):
    """
    Decrypts RC4 ciphertext using a 40-128 bit key

    :param key:
        The encryption key - a byte string 5-16 bytes long

    :param data:
        The ciphertext - a byte string

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by OpenSSL

    :return:
        A byte string of the plaintext
    """

    if len(key) < 5 or len(key) > 16:
        raise ValueError(pretty_message(
            '''
            key must be 5 to 16 bytes (40 to 128 bits) long - is %s
            ''',
            len(key)
        ))

    return _decrypt('rc4', key, data, None, None)