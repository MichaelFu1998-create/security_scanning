def aes_cbc_no_padding_decrypt(key, data, iv):
    """
    Decrypts AES ciphertext in CBC mode using a 128, 192 or 256 bit key and no
    padding.

    :param key:
        The encryption key - a byte string either 16, 24 or 32 bytes long

    :param data:
        The ciphertext - a byte string

    :param iv:
        The initialization vector - a byte string 16-bytes long

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by OpenSSL

    :return:
        A byte string of the plaintext
    """

    cipher = _calculate_aes_cipher(key)

    if len(iv) != 16:
        raise ValueError(pretty_message(
            '''
            iv must be 16 bytes long - is %s
            ''',
            len(iv)
        ))

    return _decrypt(cipher, key, data, iv, False)