def add_pss_padding(hash_algorithm, salt_length, key_length, message):
    """
    Pads a byte string using the EMSA-PSS-Encode operation described in PKCS#1
    v2.2.

    :param hash_algorithm:
        The string name of the hash algorithm to use: "sha1", "sha224",
        "sha256", "sha384", "sha512"

    :param salt_length:
        The length of the salt as an integer - typically the same as the length
        of the output from the hash_algorithm

    :param key_length:
        The length of the RSA key, in bits

    :param message:
        A byte string of the message to pad

    :return:
        The encoded (passed) message
    """

    if _backend != 'winlegacy' and sys.platform != 'darwin':
        raise SystemError(pretty_message(
            '''
            Pure-python RSA PSS signature padding addition code is only for
            Windows XP/2003 and OS X
            '''
        ))

    if not isinstance(message, byte_cls):
        raise TypeError(pretty_message(
            '''
            message must be a byte string, not %s
            ''',
            type_name(message)
        ))

    if not isinstance(salt_length, int_types):
        raise TypeError(pretty_message(
            '''
            salt_length must be an integer, not %s
            ''',
            type_name(salt_length)
        ))

    if salt_length < 0:
        raise ValueError(pretty_message(
            '''
            salt_length must be 0 or more - is %s
            ''',
            repr(salt_length)
        ))

    if not isinstance(key_length, int_types):
        raise TypeError(pretty_message(
            '''
            key_length must be an integer, not %s
            ''',
            type_name(key_length)
        ))

    if key_length < 512:
        raise ValueError(pretty_message(
            '''
            key_length must be 512 or more - is %s
            ''',
            repr(key_length)
        ))

    if hash_algorithm not in set(['sha1', 'sha224', 'sha256', 'sha384', 'sha512']):
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of "sha1", "sha224", "sha256", "sha384",
            "sha512", not %s
            ''',
            repr(hash_algorithm)
        ))

    hash_func = getattr(hashlib, hash_algorithm)

    # The maximal bit size of a non-negative integer is one less than the bit
    # size of the key since the first bit is used to store sign
    em_bits = key_length - 1
    em_len = int(math.ceil(em_bits / 8))

    message_digest = hash_func(message).digest()
    hash_length = len(message_digest)

    if em_len < hash_length + salt_length + 2:
        raise ValueError(pretty_message(
            '''
            Key is not long enough to use with specified hash_algorithm and
            salt_length
            '''
        ))

    if salt_length > 0:
        salt = os.urandom(salt_length)
    else:
        salt = b''

    m_prime = (b'\x00' * 8) + message_digest + salt

    m_prime_digest = hash_func(m_prime).digest()

    padding = b'\x00' * (em_len - salt_length - hash_length - 2)

    db = padding + b'\x01' + salt

    db_mask = _mgf1(hash_algorithm, m_prime_digest, em_len - hash_length - 1)

    masked_db = int_to_bytes(int_from_bytes(db) ^ int_from_bytes(db_mask))
    masked_db = fill_width(masked_db, len(db_mask))

    zero_bits = (8 * em_len) - em_bits
    left_bit_mask = ('0' * zero_bits) + ('1' * (8 - zero_bits))
    left_int_mask = int(left_bit_mask, 2)

    if left_int_mask != 255:
        masked_db = chr_cls(left_int_mask & ord(masked_db[0:1])) + masked_db[1:]

    return masked_db + m_prime_digest + b'\xBC'