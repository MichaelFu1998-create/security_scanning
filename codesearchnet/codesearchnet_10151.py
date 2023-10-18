def pbkdf1(hash_algorithm, password, salt, iterations, key_length):
    """
    An implementation of PBKDF1 - should only be used for interop with legacy
    systems, not new architectures

    :param hash_algorithm:
        The string name of the hash algorithm to use: "md2", "md5", "sha1"

    :param password:
        A byte string of the password to use an input to the KDF

    :param salt:
        A cryptographic random byte string

    :param iterations:
        The numbers of iterations to use when deriving the key

    :param key_length:
        The length of the desired key in bytes

    :return:
        The derived key as a byte string
    """

    if not isinstance(password, byte_cls):
        raise TypeError(pretty_message(
            '''
            password must be a byte string, not %s
            ''',
            (type_name(password))
        ))

    if not isinstance(salt, byte_cls):
        raise TypeError(pretty_message(
            '''
            salt must be a byte string, not %s
            ''',
            (type_name(salt))
        ))

    if not isinstance(iterations, int_types):
        raise TypeError(pretty_message(
            '''
            iterations must be an integer, not %s
            ''',
            (type_name(iterations))
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
            (type_name(key_length))
        ))

    if key_length < 1:
        raise ValueError(pretty_message(
            '''
            key_length must be greater than 0 - is %s
            ''',
            repr(key_length)
        ))

    if hash_algorithm not in set(['md2', 'md5', 'sha1']):
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of "md2", "md5", "sha1", not %s
            ''',
            repr(hash_algorithm)
        ))

    if key_length > 16 and hash_algorithm in set(['md2', 'md5']):
        raise ValueError(pretty_message(
            '''
            key_length can not be longer than 16 for %s - is %s
            ''',
            (hash_algorithm, repr(key_length))
        ))

    if key_length > 20 and hash_algorithm == 'sha1':
        raise ValueError(pretty_message(
            '''
            key_length can not be longer than 20 for sha1 - is %s
            ''',
            repr(key_length)
        ))

    algo = getattr(hashlib, hash_algorithm)
    output = algo(password + salt).digest()
    for _ in range(2, iterations + 1):
        output = algo(output).digest()

    return output[:key_length]