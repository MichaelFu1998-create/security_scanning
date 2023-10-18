def ecdsa_verify(certificate_or_public_key, signature, data, hash_algorithm):
    """
    Verifies an ECDSA signature in pure Python (thus slow)

    :param certificate_or_public_key:
        A Certificate or PublicKey instance to verify the signature with

    :param signature:
        A byte string of the signature to verify

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha256", "sha384" or "sha512"

    :raises:
        oscrypto.errors.SignatureError - when the signature is determined to be invalid
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library
    """

    has_asn1 = hasattr(certificate_or_public_key, 'asn1')
    if not has_asn1 or not isinstance(certificate_or_public_key.asn1, (keys.PublicKeyInfo, Certificate)):
        raise TypeError(pretty_message(
            '''
            certificate_or_public_key must be an instance of the
            oscrypto.asymmetric.PublicKey or oscrypto.asymmetric.Certificate
            classes, not %s
            ''',
            type_name(certificate_or_public_key)
        ))

    curve_name = certificate_or_public_key.curve
    if curve_name not in set(['secp256r1', 'secp384r1', 'secp521r1']):
        raise ValueError(pretty_message(
            '''
            certificate_or_public_key does not use one of the named curves
            secp256r1, secp384r1 or secp521r1
            '''
        ))

    if not isinstance(signature, byte_cls):
        raise TypeError(pretty_message(
            '''
            signature must be a byte string, not %s
            ''',
            type_name(signature)
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

    asn1 = certificate_or_public_key.asn1
    if isinstance(asn1, Certificate):
        asn1 = asn1.public_key

    curve_base_point = {
        'secp256r1': SECP256R1_BASE_POINT,
        'secp384r1': SECP384R1_BASE_POINT,
        'secp521r1': SECP521R1_BASE_POINT,
    }[curve_name]

    x, y = asn1['public_key'].to_coords()
    n = curve_base_point.order

    # Validates that the point is valid
    public_key_point = PrimePoint(curve_base_point.curve, x, y, n)

    try:
        signature = DSASignature.load(signature)
        r = signature['r'].native
        s = signature['s'].native
    except (ValueError):
        raise SignatureError('Signature is invalid')

    invalid = 0

    # Check r is valid
    invalid |= r < 1
    invalid |= r >= n

    # Check s is valid
    invalid |= s < 1
    invalid |= s >= n

    if invalid:
        raise SignatureError('Signature is invalid')

    hash_func = getattr(hashlib, hash_algorithm)

    digest = hash_func(data).digest()

    z = int_from_bytes(digest, signed=False) % n
    w = inverse_mod(s, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    hash_point = (curve_base_point * u1) + (public_key_point * u2)
    if r != (hash_point.x % n):
        raise SignatureError('Signature is invalid')