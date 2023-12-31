def pkcs12_kdf(hash_algorithm, password, salt, iterations, key_length, id_):
    """
    KDF from RFC7292 appendix B.2 - https://tools.ietf.org/html/rfc7292#page-19

    :param hash_algorithm:
        The string name of the hash algorithm to use: "md5", "sha1", "sha224", "sha256", "sha384", "sha512"

    :param password:
        A byte string of the password to use an input to the KDF

    :param salt:
        A cryptographic random byte string

    :param iterations:
        The numbers of iterations to use when deriving the key

    :param key_length:
        The length of the desired key in bytes

    :param id_:
        The ID of the usage - 1 for key, 2 for iv, 3 for mac

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type

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
        raise ValueError(pretty_message(
            '''
            iterations must be greater than 0 - is %s
            ''',
            repr(iterations)
        ))

    if not isinstance(key_length, int_types):
        raise TypeError(pretty_message(
            '''
            key_length must be an integer, not %s
            ''',
            type_name(key_length)
        ))

    if key_length < 1:
        raise ValueError(pretty_message(
            '''
            key_length must be greater than 0 - is %s
            ''',
            repr(key_length)
        ))

    if hash_algorithm not in set(['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512']):
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of "md5", "sha1", "sha224", "sha256",
            "sha384", "sha512", not %s
            ''',
            repr(hash_algorithm)
        ))

    if id_ not in set([1, 2, 3]):
        raise ValueError(pretty_message(
            '''
            id_ must be one of 1, 2, 3, not %s
            ''',
            repr(id_)
        ))

    utf16_password = password.decode('utf-8').encode('utf-16be') + b'\x00\x00'

    digest_type = {
        'md5': libcrypto.EVP_md5,
        'sha1': libcrypto.EVP_sha1,
        'sha224': libcrypto.EVP_sha224,
        'sha256': libcrypto.EVP_sha256,
        'sha384': libcrypto.EVP_sha384,
        'sha512': libcrypto.EVP_sha512,
    }[hash_algorithm]()

    output_buffer = buffer_from_bytes(key_length)
    result = libcrypto.PKCS12_key_gen_uni(
        utf16_password,
        len(utf16_password),
        salt,
        len(salt),
        id_,
        iterations,
        key_length,
        output_buffer,
        digest_type
    )
    handle_openssl_error(result)

    return bytes_from_buffer(output_buffer)