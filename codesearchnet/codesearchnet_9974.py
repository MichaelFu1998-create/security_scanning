def _encrypt(certificate_or_public_key, data, padding):
    """
    Encrypts plaintext using an RSA public key or certificate

    :param certificate_or_public_key:
        A PublicKey, Certificate or PrivateKey object

    :param data:
        The byte string to encrypt

    :param padding:
        The padding mode to use

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the encrypted data
    """

    if not isinstance(certificate_or_public_key, (Certificate, PublicKey)):
        raise TypeError(pretty_message(
            '''
            certificate_or_public_key must be an instance of the Certificate or
            PublicKey class, not %s
            ''',
            type_name(certificate_or_public_key)
        ))

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    rsa = None

    try:
        buffer_size = libcrypto.EVP_PKEY_size(certificate_or_public_key.evp_pkey)
        buffer = buffer_from_bytes(buffer_size)

        rsa = libcrypto.EVP_PKEY_get1_RSA(certificate_or_public_key.evp_pkey)
        res = libcrypto.RSA_public_encrypt(len(data), data, buffer, rsa, padding)
        handle_openssl_error(res)

        return bytes_from_buffer(buffer, res)

    finally:
        if rsa:
            libcrypto.RSA_free(rsa)