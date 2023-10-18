def _mgf1(hash_algorithm, seed, mask_length):
    """
    The PKCS#1 MGF1 mask generation algorithm

    :param hash_algorithm:
        The string name of the hash algorithm to use: "sha1", "sha224",
        "sha256", "sha384", "sha512"

    :param seed:
        A byte string to use as the seed for the mask

    :param mask_length:
        The desired mask length, as an integer

    :return:
        A byte string of the mask
    """

    if not isinstance(seed, byte_cls):
        raise TypeError(pretty_message(
            '''
            seed must be a byte string, not %s
            ''',
            type_name(seed)
        ))

    if not isinstance(mask_length, int_types):
        raise TypeError(pretty_message(
            '''
            mask_length must be an integer, not %s
            ''',
            type_name(mask_length)
        ))

    if mask_length < 1:
        raise ValueError(pretty_message(
            '''
            mask_length must be greater than 0 - is %s
            ''',
            repr(mask_length)
        ))

    if hash_algorithm not in set(['sha1', 'sha224', 'sha256', 'sha384', 'sha512']):
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of "sha1", "sha224", "sha256", "sha384",
            "sha512", not %s
            ''',
            repr(hash_algorithm)
        ))

    output = b''

    hash_length = {
        'sha1': 20,
        'sha224': 28,
        'sha256': 32,
        'sha384': 48,
        'sha512': 64
    }[hash_algorithm]

    iterations = int(math.ceil(mask_length / hash_length))

    pack = struct.Struct(b'>I').pack
    hash_func = getattr(hashlib, hash_algorithm)

    for counter in range(0, iterations):
        b = pack(counter)
        output += hash_func(seed + b).digest()

    return output[0:mask_length]