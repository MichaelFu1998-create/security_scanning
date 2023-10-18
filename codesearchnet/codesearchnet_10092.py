def ec_generate_pair(curve):
    """
    Generates a EC public/private key pair

    :param curve:
        A unicode string. Valid values include "secp256r1", "secp384r1" and
        "secp521r1".

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type

    :return:
        A 2-element tuple of (asn1crypto.keys.PublicKeyInfo,
        asn1crypto.keys.PrivateKeyInfo)
    """

    if curve not in set(['secp256r1', 'secp384r1', 'secp521r1']):
        raise ValueError(pretty_message(
            '''
            curve must be one of "secp256r1", "secp384r1", "secp521r1", not %s
            ''',
            repr(curve)
        ))

    curve_num_bytes = CURVE_BYTES[curve]
    curve_base_point = {
        'secp256r1': SECP256R1_BASE_POINT,
        'secp384r1': SECP384R1_BASE_POINT,
        'secp521r1': SECP521R1_BASE_POINT,
    }[curve]

    while True:
        private_key_bytes = rand_bytes(curve_num_bytes)
        private_key_int = int_from_bytes(private_key_bytes, signed=False)

        if private_key_int > 0 and private_key_int < curve_base_point.order:
            break

    private_key_info = keys.PrivateKeyInfo({
        'version': 0,
        'private_key_algorithm': keys.PrivateKeyAlgorithm({
            'algorithm': 'ec',
            'parameters': keys.ECDomainParameters(
                name='named',
                value=curve
            )
        }),
        'private_key': keys.ECPrivateKey({
            'version': 'ecPrivkeyVer1',
            'private_key': private_key_int
        }),
    })
    private_key_info['private_key'].parsed['public_key'] = private_key_info.public_key
    public_key_info = private_key_info.public_key_info

    return (public_key_info, private_key_info)