def _decrypt(private_key, ciphertext, padding):
    """
    Decrypts RSA ciphertext using a private key

    :param private_key:
        A PrivateKey object

    :param ciphertext:
        The ciphertext - a byte string

    :param padding:
        The padding mode to use

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the plaintext
    """

    if not isinstance(private_key, PrivateKey):
        raise TypeError(pretty_message(
            '''
            private_key must be an instance of the PrivateKey class, not %s
            ''',
            type_name(private_key)
        ))

    if not isinstance(ciphertext, byte_cls):
        raise TypeError(pretty_message(
            '''
            ciphertext must be a byte string, not %s
            ''',
            type_name(ciphertext)
        ))

    rsa = None

    try:
        buffer_size = libcrypto.EVP_PKEY_size(private_key.evp_pkey)
        buffer = buffer_from_bytes(buffer_size)

        rsa = libcrypto.EVP_PKEY_get1_RSA(private_key.evp_pkey)
        res = libcrypto.RSA_private_decrypt(len(ciphertext), ciphertext, buffer, rsa, padding)
        handle_openssl_error(res)

        return bytes_from_buffer(buffer, res)

    finally:
        if rsa:
            libcrypto.RSA_free(rsa)