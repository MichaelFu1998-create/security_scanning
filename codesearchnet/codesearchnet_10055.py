def verify_pss_padding(hash_algorithm, salt_length, key_length, message, signature):
    """
    Verifies the PSS padding on an encoded message

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

    :param signature:
        The signature to verify

    :return:
        A boolean indicating if the signature is invalid
    """

    if _backend != 'winlegacy' and sys.platform != 'darwin':
        raise SystemError(pretty_message(
            '''
            Pure-python RSA PSS signature padding verification code is only for
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

    if not isinstance(signature, byte_cls):
        raise TypeError(pretty_message(
            '''
            signature must be a byte string, not %s
            ''',
            type_name(signature)
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

    if hash_algorithm not in set(['sha1', 'sha224', 'sha256', 'sha384', 'sha512']):
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of "sha1", "sha224", "sha256", "sha384",
            "sha512", not %s
            ''',
            repr(hash_algorithm)
        ))

    hash_func = getattr(hashlib, hash_algorithm)

    em_bits = key_length - 1
    em_len = int(math.ceil(em_bits / 8))

    message_digest = hash_func(message).digest()
    hash_length = len(message_digest)

    if em_len < hash_length + salt_length + 2:
        return False

    if signature[-1:] != b'\xBC':
        return False

    zero_bits = (8 * em_len) - em_bits

    masked_db_length = em_len - hash_length - 1
    masked_db = signature[0:masked_db_length]

    first_byte = ord(masked_db[0:1])
    bits_that_should_be_zero = first_byte >> (8 - zero_bits)
    if bits_that_should_be_zero != 0:
        return False

    m_prime_digest = signature[masked_db_length:masked_db_length + hash_length]

    db_mask = _mgf1(hash_algorithm, m_prime_digest, em_len - hash_length - 1)

    left_bit_mask = ('0' * zero_bits) + ('1' * (8 - zero_bits))
    left_int_mask = int(left_bit_mask, 2)

    if left_int_mask != 255:
        db_mask = chr_cls(left_int_mask & ord(db_mask[0:1])) + db_mask[1:]

    db = int_to_bytes(int_from_bytes(masked_db) ^ int_from_bytes(db_mask))
    if len(db) < len(masked_db):
        db = (b'\x00' * (len(masked_db) - len(db))) + db

    zero_length = em_len - hash_length - salt_length - 2
    zero_string = b'\x00' * zero_length
    if not constant_compare(db[0:zero_length], zero_string):
        return False

    if db[zero_length:zero_length + 1] != b'\x01':
        return False

    salt = db[0 - salt_length:]

    m_prime = (b'\x00' * 8) + message_digest + salt

    h_prime = hash_func(m_prime).digest()

    return constant_compare(m_prime_digest, h_prime)