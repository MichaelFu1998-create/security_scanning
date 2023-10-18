def rsa_pss_verify(certificate_or_public_key, signature, data, hash_algorithm):
    """
    Verifies an RSASSA-PSS signature. For the PSS padding the mask gen algorithm
    will be mgf1 using the same hash algorithm as the signature. The salt length
    with be the length of the hash algorithm, and the trailer field with be the
    standard 0xBC byte.

    :param certificate_or_public_key:
        A Certificate or PublicKey instance to verify the signature with

    :param signature:
        A byte string of the signature to verify

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha224", "sha256", "sha384" or "sha512"

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

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    if certificate_or_public_key.algorithm != 'rsa':
        raise ValueError('The key specified is not an RSA public key')

    hash_length = {
        'sha1': 20,
        'sha224': 28,
        'sha256': 32,
        'sha384': 48,
        'sha512': 64
    }.get(hash_algorithm, 0)

    key_length = certificate_or_public_key.byte_size
    buffer = buffer_from_bytes(key_length)
    output_length = new(Security, 'size_t *', key_length)
    result = Security.SecKeyEncrypt(
        certificate_or_public_key.sec_key_ref,
        SecurityConst.kSecPaddingNone,
        signature,
        len(signature),
        buffer,
        output_length
    )
    handle_sec_error(result)

    plaintext = bytes_from_buffer(buffer, deref(output_length))
    if not verify_pss_padding(hash_algorithm, hash_length, certificate_or_public_key.bit_size, data, plaintext):
        raise SignatureError('Signature is invalid')