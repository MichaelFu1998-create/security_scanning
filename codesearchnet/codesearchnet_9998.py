def _verify(certificate_or_public_key, signature, data, hash_algorithm, rsa_pss_padding=False):
    """
    Verifies an RSA, DSA or ECDSA signature

    :param certificate_or_public_key:
        A Certificate or PublicKey instance to verify the signature with

    :param signature:
        A byte string of the signature to verify

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha256", "sha384", "sha512" or "raw"

    :param rsa_pss_padding:
        If PSS padding should be used for RSA keys

    :raises:
        oscrypto.errors.SignatureError - when the signature is determined to be invalid
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library
    """

    if not isinstance(certificate_or_public_key, (Certificate, PublicKey)):
        raise TypeError(pretty_message(
            '''
            certificate_or_public_key must be an instance of the Certificate or
            PublicKey class, not %s
            ''',
            type_name(certificate_or_public_key)
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

    valid_hash_algorithms = set(['md5', 'sha1', 'sha256', 'sha384', 'sha512'])
    if certificate_or_public_key.algorithm == 'rsa' and not rsa_pss_padding:
        valid_hash_algorithms |= set(['raw'])

    if hash_algorithm not in valid_hash_algorithms:
        valid_hash_algorithms_error = '"md5", "sha1", "sha256", "sha384", "sha512"'
        if certificate_or_public_key.algorithm == 'rsa' and not rsa_pss_padding:
            valid_hash_algorithms_error += ', "raw"'
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of %s, not %s
            ''',
            valid_hash_algorithms_error,
            repr(hash_algorithm)
        ))

    if certificate_or_public_key.algorithm != 'rsa' and rsa_pss_padding is not False:
        raise ValueError(pretty_message(
            '''
            PSS padding may only be used with RSA keys - signing via a %s key
            was requested
            ''',
            certificate_or_public_key.algorithm.upper()
        ))

    if hash_algorithm == 'raw':
        if len(data) > certificate_or_public_key.byte_size - 11:
            raise ValueError(pretty_message(
                '''
                data must be 11 bytes shorter than the key size when
                hash_algorithm is "raw" - key size is %s bytes, but
                data is %s bytes long
                ''',
                certificate_or_public_key.byte_size,
                len(data)
            ))

    if _backend == 'winlegacy':
        if certificate_or_public_key.algorithm == 'ec':
            return _pure_python_ecdsa_verify(certificate_or_public_key, signature, data, hash_algorithm)
        return _advapi32_verify(certificate_or_public_key, signature, data, hash_algorithm, rsa_pss_padding)
    return _bcrypt_verify(certificate_or_public_key, signature, data, hash_algorithm, rsa_pss_padding)