def pbkdf2(hash_algorithm, password, salt, iterations, key_length):
    """
    PBKDF2 from PKCS#5

    :param hash_algorithm:
        The string name of the hash algorithm to use: "sha1", "sha224", "sha256", "sha384", "sha512"

    :param password:
        A byte string of the password to use an input to the KDF

    :param salt:
        A cryptographic random byte string

    :param iterations:
        The numbers of iterations to use when deriving the key

    :param key_length:
        The length of the desired key in bytes

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        The derived key as a byte string
    """

    if not isinstance(password, byte_cls):
        raise TypeError(pretty_message(
            '''
            password must be a byte string, not %s
            ''',
            type_name(password)
        ))

    if not isinstance(salt, byte_cls):
        raise TypeError(pretty_message(
            '''
            salt must be a byte string, not %s
            ''',
            type_name(salt)
        ))

    if not isinstance(iterations, int_types):
        raise TypeError(pretty_message(
            '''
            iterations must be an integer, not %s
            ''',
            type_name(iterations)
        ))

    if iterations < 1:
        raise ValueError('iterations must be greater than 0')

    if not isinstance(key_length, int_types):
        raise TypeError(pretty_message(
            '''
            key_length must be an integer, not %s
            ''',
            type_name(key_length)
        ))

    if key_length < 1:
        raise ValueError('key_length must be greater than 0')

    if hash_algorithm not in set(['sha1', 'sha224', 'sha256', 'sha384', 'sha512']):
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of "sha1", "sha224", "sha256", "sha384",
            "sha512", not %s
            ''',
            repr(hash_algorithm)
        ))

    algo = {
        'sha1': CommonCryptoConst.kCCPRFHmacAlgSHA1,
        'sha224': CommonCryptoConst.kCCPRFHmacAlgSHA224,
        'sha256': CommonCryptoConst.kCCPRFHmacAlgSHA256,
        'sha384': CommonCryptoConst.kCCPRFHmacAlgSHA384,
        'sha512': CommonCryptoConst.kCCPRFHmacAlgSHA512
    }[hash_algorithm]

    output_buffer = buffer_from_bytes(key_length)
    result = CommonCrypto.CCKeyDerivationPBKDF(
        CommonCryptoConst.kCCPBKDF2,
        password,
        len(password),
        salt,
        len(salt),
        algo,
        iterations,
        output_buffer,
        key_length
    )
    if result != 0:
        raise OSError(_extract_error())

    return bytes_from_buffer(output_buffer)