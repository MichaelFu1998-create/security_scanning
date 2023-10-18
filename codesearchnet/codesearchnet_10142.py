def _verify(certificate_or_public_key, signature, data, hash_algorithm):
    """
    Verifies an RSA, DSA or ECDSA signature

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

    valid_hash_algorithms = set(['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'])
    if certificate_or_public_key.algorithm == 'rsa':
        valid_hash_algorithms |= set(['raw'])

    if hash_algorithm not in valid_hash_algorithms:
        valid_hash_algorithms_error = '"md5", "sha1", "sha224", "sha256", "sha384", "sha512"'
        if certificate_or_public_key.algorithm == 'rsa':
            valid_hash_algorithms_error += ', "raw"'
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of %s, not %s
            ''',
            valid_hash_algorithms_error,
            repr(hash_algorithm)
        ))

    if certificate_or_public_key.algorithm == 'rsa' and hash_algorithm == 'raw':
        if len(data) > certificate_or_public_key.byte_size - 11:
            raise ValueError(pretty_message(
                '''
                data must be 11 bytes shorter than the key size when
                hash_algorithm is "raw" - key size is %s bytes, but data
                is %s bytes long
                ''',
                certificate_or_public_key.byte_size,
                len(data)
            ))

        result = Security.SecKeyRawVerify(
            certificate_or_public_key.sec_key_ref,
            SecurityConst.kSecPaddingPKCS1,
            data,
            len(data),
            signature,
            len(signature)
        )
        # errSSLCrypto is returned in some situations on macOS 10.12
        if result == SecurityConst.errSecVerifyFailed or result == SecurityConst.errSSLCrypto:
            raise SignatureError('Signature is invalid')
        handle_sec_error(result)
        return

    cf_signature = None
    cf_data = None
    cf_hash_length = None
    sec_transform = None

    try:
        error_pointer = new(CoreFoundation, 'CFErrorRef *')
        cf_signature = CFHelpers.cf_data_from_bytes(signature)
        sec_transform = Security.SecVerifyTransformCreate(
            certificate_or_public_key.sec_key_ref,
            cf_signature,
            error_pointer
        )
        handle_cf_error(error_pointer)

        hash_constant = {
            'md5': Security.kSecDigestMD5,
            'sha1': Security.kSecDigestSHA1,
            'sha224': Security.kSecDigestSHA2,
            'sha256': Security.kSecDigestSHA2,
            'sha384': Security.kSecDigestSHA2,
            'sha512': Security.kSecDigestSHA2
        }[hash_algorithm]

        Security.SecTransformSetAttribute(
            sec_transform,
            Security.kSecDigestTypeAttribute,
            hash_constant,
            error_pointer
        )
        handle_cf_error(error_pointer)

        if hash_algorithm in set(['sha224', 'sha256', 'sha384', 'sha512']):
            hash_length = {
                'sha224': 224,
                'sha256': 256,
                'sha384': 384,
                'sha512': 512
            }[hash_algorithm]

            cf_hash_length = CFHelpers.cf_number_from_integer(hash_length)

            Security.SecTransformSetAttribute(
                sec_transform,
                Security.kSecDigestLengthAttribute,
                cf_hash_length,
                error_pointer
            )
            handle_cf_error(error_pointer)

        if certificate_or_public_key.algorithm == 'rsa':
            Security.SecTransformSetAttribute(
                sec_transform,
                Security.kSecPaddingKey,
                Security.kSecPaddingPKCS1Key,
                error_pointer
            )
            handle_cf_error(error_pointer)

        cf_data = CFHelpers.cf_data_from_bytes(data)
        Security.SecTransformSetAttribute(
            sec_transform,
            Security.kSecTransformInputAttributeName,
            cf_data,
            error_pointer
        )
        handle_cf_error(error_pointer)

        res = Security.SecTransformExecute(sec_transform, error_pointer)
        if not is_null(error_pointer):
            error = unwrap(error_pointer)
            if not is_null(error):
                raise SignatureError('Signature is invalid')

        res = bool(CoreFoundation.CFBooleanGetValue(res))

        if not res:
            raise SignatureError('Signature is invalid')

    finally:
        if sec_transform:
            CoreFoundation.CFRelease(sec_transform)
        if cf_signature:
            CoreFoundation.CFRelease(cf_signature)
        if cf_data:
            CoreFoundation.CFRelease(cf_data)
        if cf_hash_length:
            CoreFoundation.CFRelease(cf_hash_length)