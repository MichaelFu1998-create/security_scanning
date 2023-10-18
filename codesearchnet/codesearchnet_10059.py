def raw_rsa_private_crypt(private_key, data):
    """
    Performs a raw RSA algorithm in a byte string using a private key.
    This is a low-level primitive and is prone to disastrous results if used
    incorrectly.

    :param private_key:
        An oscrypto.asymmetric.PrivateKey object

    :param data:
        A byte string of the plaintext to be signed or ciphertext to be
        decrypted. Must be less than or equal to the length of the private key.
        In the case of signing, padding must already be applied. In the case of
        decryption, padding must be removed afterward.

    :return:
        A byte string of the transformed data
    """

    if _backend != 'winlegacy':
        raise SystemError('Pure-python RSA crypt is only for Windows XP/2003')

    if not hasattr(private_key, 'asn1') or not isinstance(private_key.asn1, PrivateKeyInfo):
        raise TypeError(pretty_message(
            '''
            private_key must be an instance of the
            oscrypto.asymmetric.PrivateKey class, not %s
            ''',
            type_name(private_key)
        ))

    algo = private_key.asn1['private_key_algorithm']['algorithm'].native
    if algo != 'rsa':
        raise ValueError(pretty_message(
            '''
            private_key must be an RSA key, not %s
            ''',
            algo.upper()
        ))

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    rsa_private_key = private_key.asn1['private_key'].parsed
    transformed_int = pow(
        int_from_bytes(data),
        rsa_private_key['private_exponent'].native,
        rsa_private_key['modulus'].native
    )
    return int_to_bytes(transformed_int, width=private_key.asn1.byte_size)