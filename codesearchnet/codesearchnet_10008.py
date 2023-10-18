def _encrypt(certificate_or_public_key, data, rsa_oaep_padding=False):
    """
    Encrypts a value using an RSA public key

    :param certificate_or_public_key:
        A Certificate or PublicKey instance to encrypt with

    :param data:
        A byte string of the data to encrypt

    :param rsa_oaep_padding:
        If OAEP padding should be used instead of PKCS#1 v1.5

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the ciphertext
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

    if not isinstance(rsa_oaep_padding, bool):
        raise TypeError(pretty_message(
            '''
            rsa_oaep_padding must be a bool, not %s
            ''',
            type_name(rsa_oaep_padding)
        ))

    if _backend == 'winlegacy':
        return _advapi32_encrypt(certificate_or_public_key, data, rsa_oaep_padding)
    return _bcrypt_encrypt(certificate_or_public_key, data, rsa_oaep_padding)