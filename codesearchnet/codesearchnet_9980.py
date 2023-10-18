def generate_pair(algorithm, bit_size=None, curve=None):
    """
    Generates a public/private key pair

    :param algorithm:
        The key algorithm - "rsa", "dsa" or "ec"

    :param bit_size:
        An integer - used for "rsa" and "dsa". For "rsa" the value maye be 1024,
        2048, 3072 or 4096. For "dsa" the value may be 1024, plus 2048 or 3072
        if on Windows 8 or newer.

    :param curve:
        A unicode string - used for "ec" keys. Valid values include "secp256r1",
        "secp384r1" and "secp521r1".

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A 2-element tuple of (PublicKey, PrivateKey). The contents of each key
        may be saved by calling .asn1.dump().
    """

    if algorithm not in set(['rsa', 'dsa', 'ec']):
        raise ValueError(pretty_message(
            '''
            algorithm must be one of "rsa", "dsa", "ec", not %s
            ''',
            repr(algorithm)
        ))

    if algorithm == 'rsa':
        if bit_size not in set([1024, 2048, 3072, 4096]):
            raise ValueError(pretty_message(
                '''
                bit_size must be one of 1024, 2048, 3072, 4096, not %s
                ''',
                repr(bit_size)
            ))

    elif algorithm == 'dsa':
        # Windows Vista and 7 only support SHA1-based DSA keys
        if _win_version_info < (6, 2) or _backend == 'winlegacy':
            if bit_size != 1024:
                raise ValueError(pretty_message(
                    '''
                    bit_size must be 1024, not %s
                    ''',
                    repr(bit_size)
                ))
        else:
            if bit_size not in set([1024, 2048, 3072]):
                raise ValueError(pretty_message(
                    '''
                    bit_size must be one of 1024, 2048, 3072, not %s
                    ''',
                    repr(bit_size)
                ))

    elif algorithm == 'ec':
        if curve not in set(['secp256r1', 'secp384r1', 'secp521r1']):
            raise ValueError(pretty_message(
                '''
                curve must be one of "secp256r1", "secp384r1", "secp521r1", not %s
                ''',
                repr(curve)
            ))

    if _backend == 'winlegacy':
        if algorithm == 'ec':
            pub_info, priv_info = _pure_python_ec_generate_pair(curve)
            return (PublicKey(None, pub_info), PrivateKey(None, priv_info))
        return _advapi32_generate_pair(algorithm, bit_size)
    else:
        return _bcrypt_generate_pair(algorithm, bit_size, curve)