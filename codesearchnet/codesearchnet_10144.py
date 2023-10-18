def _sign(private_key, data, hash_algorithm):
    """
    Generates an RSA, DSA or ECDSA signature

    :param private_key:
        The PrivateKey to generate the signature with

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha224", "sha256", "sha384" or
        "sha512"

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the signature
    """

    if not isinstance(private_key, PrivateKey):
        raise TypeError(pretty_message(
            '''
            private_key must be an instance of PrivateKey, not %s
            ''',
            type_name(private_key)
        ))

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    valid_hash_algorithms = set(['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'])
    if private_key.algorithm == 'rsa':
        valid_hash_algorithms |= set(['raw'])

    if hash_algorithm not in valid_hash_algorithms:
        valid_hash_algorithms_error = '"md5", "sha1", "sha224", "sha256", "sha384", "sha512"'
        if private_key.algorithm == 'rsa':
            valid_hash_algorithms_error += ', "raw"'
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of %s, not %s
            ''',
            valid_hash_algorithms_error,
            repr(hash_algorithm)
        ))

    if private_key.algorithm == 'rsa' and hash_algorithm == 'raw':
        if len(data) > private_key.byte_size - 11:
            raise ValueError(pretty_message(
                '''
                data must be 11 bytes shorter than the key size when
                hash_algorithm is "raw" - key size is %s bytes, but
                data is %s bytes long
                ''',
                private_key.byte_size,
                len(data)
            ))

        key_length = private_key.byte_size
        buffer = buffer_from_bytes(key_length)
        output_length = new(Security, 'size_t *', key_length)
        result = Security.SecKeyRawSign(
            private_key.sec_key_ref,
            SecurityConst.kSecPaddingPKCS1,
            data,
            len(data),
            buffer,
            output_length
        )
        handle_sec_error(result)

        return bytes_from_buffer(buffer, deref(output_length))

    cf_signature = None
    cf_data = None
    cf_hash_length = None
    sec_transform = None

    try:
        error_pointer = new(CoreFoundation, 'CFErrorRef *')
        sec_transform = Security.SecSignTransformCreate(private_key.sec_key_ref, error_pointer)
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

        if private_key.algorithm == 'rsa':
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

        cf_signature = Security.SecTransformExecute(sec_transform, error_pointer)
        handle_cf_error(error_pointer)

        return CFHelpers.cf_data_to_bytes(cf_signature)

    finally:
        if sec_transform:
            CoreFoundation.CFRelease(sec_transform)
        if cf_signature:
            CoreFoundation.CFRelease(cf_signature)
        if cf_data:
            CoreFoundation.CFRelease(cf_data)
        if cf_hash_length:
            CoreFoundation.CFRelease(cf_hash_length)