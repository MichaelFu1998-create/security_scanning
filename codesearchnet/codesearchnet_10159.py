def rc2_cbc_pkcs5_encrypt(key, data, iv):
    """
    Encrypts plaintext using RC2 with a 64 bit key

    :param key:
        The encryption key - a byte string 8 bytes long

    :param data:
        The plaintext - a byte string

    :param iv:
        The 8-byte initialization vector to use - a byte string - set as None
        to generate an appropriate one

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A tuple of two byte strings (iv, ciphertext)
    """

    if len(key) < 5 or len(key) > 16:
        raise ValueError(pretty_message(
            '''
            key must be 5 to 16 bytes (40 to 128 bits) long - is %s
            ''',
            len(key)
        ))

    if not iv:
        iv = rand_bytes(8)
    elif len(iv) != 8:
        raise ValueError(pretty_message(
            '''
            iv must be 8 bytes long - is %s
            ''',
            len(iv)
        ))

    return (iv, _encrypt(Security.kSecAttrKeyTypeRC2, key, data, iv, Security.kSecPaddingPKCS5Key))