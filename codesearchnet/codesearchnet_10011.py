def _decrypt(private_key, ciphertext, rsa_oaep_padding=False):
    """
    Encrypts a value using an RSA private key

    :param private_key:
        A PrivateKey instance to decrypt with

    :param ciphertext:
        A byte string of the data to decrypt

    :param rsa_oaep_padding:
        If OAEP padding should be used instead of PKCS#1 v1.5

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

    if not isinstance(rsa_oaep_padding, bool):
        raise TypeError(pretty_message(
            '''
            rsa_oaep_padding must be a bool, not %s
            ''',
            type_name(rsa_oaep_padding)
        ))

    if _backend == 'winlegacy':
        return _advapi32_decrypt(private_key, ciphertext, rsa_oaep_padding)
    return _bcrypt_decrypt(private_key, ciphertext, rsa_oaep_padding)