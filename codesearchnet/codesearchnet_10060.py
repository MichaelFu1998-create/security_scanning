def raw_rsa_public_crypt(certificate_or_public_key, data):
    """
    Performs a raw RSA algorithm in a byte string using a certificate or
    public key. This is a low-level primitive and is prone to disastrous results
    if used incorrectly.

    :param certificate_or_public_key:
        An oscrypto.asymmetric.PublicKey or oscrypto.asymmetric.Certificate
        object

    :param data:
        A byte string of the signature when verifying, or padded plaintext when
        encrypting. Must be less than or equal to the length of the public key.
        When verifying, padding will need to be removed afterwards. When
        encrypting, padding must be applied before.

    :return:
        A byte string of the transformed data
    """

    if _backend != 'winlegacy':
        raise SystemError('Pure-python RSA crypt is only for Windows XP/2003')

    has_asn1 = hasattr(certificate_or_public_key, 'asn1')
    valid_types = (PublicKeyInfo, Certificate)
    if not has_asn1 or not isinstance(certificate_or_public_key.asn1, valid_types):
        raise TypeError(pretty_message(
            '''
            certificate_or_public_key must be an instance of the
            oscrypto.asymmetric.PublicKey or oscrypto.asymmetric.Certificate
            classes, not %s
            ''',
            type_name(certificate_or_public_key)
        ))

    algo = certificate_or_public_key.asn1['algorithm']['algorithm'].native
    if algo != 'rsa':
        raise ValueError(pretty_message(
            '''
            certificate_or_public_key must be an RSA key, not %s
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

    rsa_public_key = certificate_or_public_key.asn1['public_key'].parsed
    transformed_int = pow(
        int_from_bytes(data),
        rsa_public_key['public_exponent'].native,
        rsa_public_key['modulus'].native
    )
    return int_to_bytes(
        transformed_int,
        width=certificate_or_public_key.asn1.byte_size
    )