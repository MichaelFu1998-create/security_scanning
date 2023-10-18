def ecdsa_sign(private_key, data, hash_algorithm):
    """
    Generates an ECDSA signature in pure Python (thus slow)

    :param private_key:
        The PrivateKey to generate the signature with

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "sha1", "sha256", "sha384" or "sha512"

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the signature
    """

    if not hasattr(private_key, 'asn1') or not isinstance(private_key.asn1, keys.PrivateKeyInfo):
        raise TypeError(pretty_message(
            '''
            private_key must be an instance of the
            oscrypto.asymmetric.PrivateKey class, not %s
            ''',
            type_name(private_key)
        ))

    curve_name = private_key.curve
    if curve_name not in set(['secp256r1', 'secp384r1', 'secp521r1']):
        raise ValueError(pretty_message(
            '''
            private_key does not use one of the named curves secp256r1,
            secp384r1 or secp521r1
            '''
        ))

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
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

    ec_private_key = private_key.asn1['private_key'].parsed
    private_key_bytes = ec_private_key['private_key'].contents
    private_key_int = ec_private_key['private_key'].native

    curve_num_bytes = CURVE_BYTES[curve_name]
    curve_base_point = {
        'secp256r1': SECP256R1_BASE_POINT,
        'secp384r1': SECP384R1_BASE_POINT,
        'secp521r1': SECP521R1_BASE_POINT,
    }[curve_name]

    n = curve_base_point.order

    # RFC 6979 section 3.2

    # a.
    digest = hash_func(data).digest()
    hash_length = len(digest)

    h = int_from_bytes(digest, signed=False) % n

    # b.
    V = b'\x01' * hash_length

    # c.
    K = b'\x00' * hash_length

    # d.
    K = hmac.new(K, V + b'\x00' + private_key_bytes + digest, hash_func).digest()

    # e.
    V = hmac.new(K, V, hash_func).digest()

    # f.
    K = hmac.new(K, V + b'\x01' + private_key_bytes + digest, hash_func).digest()

    # g.
    V = hmac.new(K, V, hash_func).digest()

    # h.
    r = 0
    s = 0
    while True:
        # h. 1
        T = b''

        # h. 2
        while len(T) < curve_num_bytes:
            V = hmac.new(K, V, hash_func).digest()
            T += V

        # h. 3
        k = int_from_bytes(T[0:curve_num_bytes], signed=False)
        if k == 0 or k >= n:
            continue

        # Calculate the signature in the loop in case we need a new k
        r = (curve_base_point * k).x % n
        if r == 0:
            continue

        s = (inverse_mod(k, n) * (h + (private_key_int * r) % n)) % n
        if s == 0:
            continue

        break

    return DSASignature({'r': r, 's': s}).dump()