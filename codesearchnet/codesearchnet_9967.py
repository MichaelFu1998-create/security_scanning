def generate_pair(algorithm, bit_size=None, curve=None):
    """
    Generates a public/private key pair

    :param algorithm:
        The key algorithm - "rsa", "dsa" or "ec"

    :param bit_size:
        An integer - used for "rsa" and "dsa". For "rsa" the value maye be 1024,
        2048, 3072 or 4096. For "dsa" the value may be 1024, plus 2048 or 3072
        if OpenSSL 1.0.0 or newer is available.

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
        if libcrypto_version_info < (1,):
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
                curve must be one of "secp256r1", "secp384r1", "secp521r1",
                not %s
                ''',
                repr(curve)
            ))

    if algorithm == 'rsa':
        rsa = None
        exponent = None

        try:
            rsa = libcrypto.RSA_new()
            if is_null(rsa):
                handle_openssl_error(0)

            exponent_pointer = new(libcrypto, 'BIGNUM **')
            result = libcrypto.BN_dec2bn(exponent_pointer, b'65537')
            handle_openssl_error(result)
            exponent = unwrap(exponent_pointer)

            result = libcrypto.RSA_generate_key_ex(rsa, bit_size, exponent, null())
            handle_openssl_error(result)

            buffer_length = libcrypto.i2d_RSAPublicKey(rsa, null())
            if buffer_length < 0:
                handle_openssl_error(buffer_length)
            buffer = buffer_from_bytes(buffer_length)
            result = libcrypto.i2d_RSAPublicKey(rsa, buffer_pointer(buffer))
            if result < 0:
                handle_openssl_error(result)
            public_key_bytes = bytes_from_buffer(buffer, buffer_length)

            buffer_length = libcrypto.i2d_RSAPrivateKey(rsa, null())
            if buffer_length < 0:
                handle_openssl_error(buffer_length)
            buffer = buffer_from_bytes(buffer_length)
            result = libcrypto.i2d_RSAPrivateKey(rsa, buffer_pointer(buffer))
            if result < 0:
                handle_openssl_error(result)
            private_key_bytes = bytes_from_buffer(buffer, buffer_length)

        finally:
            if rsa:
                libcrypto.RSA_free(rsa)
            if exponent:
                libcrypto.BN_free(exponent)

    elif algorithm == 'dsa':
        dsa = None

        try:
            dsa = libcrypto.DSA_new()
            if is_null(dsa):
                handle_openssl_error(0)

            result = libcrypto.DSA_generate_parameters_ex(dsa, bit_size, null(), 0, null(), null(), null())
            handle_openssl_error(result)

            result = libcrypto.DSA_generate_key(dsa)
            handle_openssl_error(result)

            buffer_length = libcrypto.i2d_DSA_PUBKEY(dsa, null())
            if buffer_length < 0:
                handle_openssl_error(buffer_length)
            buffer = buffer_from_bytes(buffer_length)
            result = libcrypto.i2d_DSA_PUBKEY(dsa, buffer_pointer(buffer))
            if result < 0:
                handle_openssl_error(result)
            public_key_bytes = bytes_from_buffer(buffer, buffer_length)

            buffer_length = libcrypto.i2d_DSAPrivateKey(dsa, null())
            if buffer_length < 0:
                handle_openssl_error(buffer_length)
            buffer = buffer_from_bytes(buffer_length)
            result = libcrypto.i2d_DSAPrivateKey(dsa, buffer_pointer(buffer))
            if result < 0:
                handle_openssl_error(result)
            private_key_bytes = bytes_from_buffer(buffer, buffer_length)

        finally:
            if dsa:
                libcrypto.DSA_free(dsa)

    elif algorithm == 'ec':
        ec_key = None

        try:
            curve_id = {
                'secp256r1': LibcryptoConst.NID_X9_62_prime256v1,
                'secp384r1': LibcryptoConst.NID_secp384r1,
                'secp521r1': LibcryptoConst.NID_secp521r1,
            }[curve]

            ec_key = libcrypto.EC_KEY_new_by_curve_name(curve_id)
            if is_null(ec_key):
                handle_openssl_error(0)

            result = libcrypto.EC_KEY_generate_key(ec_key)
            handle_openssl_error(result)

            libcrypto.EC_KEY_set_asn1_flag(ec_key, LibcryptoConst.OPENSSL_EC_NAMED_CURVE)

            buffer_length = libcrypto.i2o_ECPublicKey(ec_key, null())
            if buffer_length < 0:
                handle_openssl_error(buffer_length)
            buffer = buffer_from_bytes(buffer_length)
            result = libcrypto.i2o_ECPublicKey(ec_key, buffer_pointer(buffer))
            if result < 0:
                handle_openssl_error(result)
            public_key_point_bytes = bytes_from_buffer(buffer, buffer_length)

            # i2o_ECPublicKey only returns the ECPoint bytes, so we have to
            # manually wrap it in a PublicKeyInfo structure to get it to parse
            public_key = keys.PublicKeyInfo({
                'algorithm': keys.PublicKeyAlgorithm({
                    'algorithm': 'ec',
                    'parameters': keys.ECDomainParameters(
                        name='named',
                        value=curve
                    )
                }),
                'public_key': public_key_point_bytes
            })
            public_key_bytes = public_key.dump()

            buffer_length = libcrypto.i2d_ECPrivateKey(ec_key, null())
            if buffer_length < 0:
                handle_openssl_error(buffer_length)
            buffer = buffer_from_bytes(buffer_length)
            result = libcrypto.i2d_ECPrivateKey(ec_key, buffer_pointer(buffer))
            if result < 0:
                handle_openssl_error(result)
            private_key_bytes = bytes_from_buffer(buffer, buffer_length)

        finally:
            if ec_key:
                libcrypto.EC_KEY_free(ec_key)

    return (load_public_key(public_key_bytes), load_private_key(private_key_bytes))