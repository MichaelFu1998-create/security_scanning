def _decrypt(private_key, ciphertext, padding):
    """
    Decrypts RSA ciphertext using a private key

    :param private_key:
        A PrivateKey object

    :param ciphertext:
        The ciphertext - a byte string

    :param padding:
        The padding mode to use, specified as a kSecPadding*Key value

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the plaintext
    """

    if not isinstance(private_key, PrivateKey):
        raise TypeError(pretty_message(
            '''
            private_key must be an instance of the PrivateKey class, not %s
            ''',
            type_name(private_key)
        ))

    if not isinstance(ciphertext, byte_cls):
        raise TypeError(pretty_message(
            '''
            ciphertext must be a byte string, not %s
            ''',
            type_name(ciphertext)
        ))

    if not padding:
        raise ValueError('padding must be specified')

    cf_data = None
    sec_transform = None

    try:
        cf_data = CFHelpers.cf_data_from_bytes(ciphertext)

        error_pointer = new(CoreFoundation, 'CFErrorRef *')
        sec_transform = Security.SecDecryptTransformCreate(
            private_key.sec_key_ref,
            error_pointer
        )
        handle_cf_error(error_pointer)

        Security.SecTransformSetAttribute(
            sec_transform,
            Security.kSecPaddingKey,
            padding,
            error_pointer
        )
        handle_cf_error(error_pointer)

        Security.SecTransformSetAttribute(
            sec_transform,
            Security.kSecTransformInputAttributeName,
            cf_data,
            error_pointer
        )
        handle_cf_error(error_pointer)

        plaintext = Security.SecTransformExecute(sec_transform, error_pointer)
        handle_cf_error(error_pointer)

        return CFHelpers.cf_data_to_bytes(plaintext)

    finally:
        if cf_data:
            CoreFoundation.CFRelease(cf_data)
        if sec_transform:
            CoreFoundation.CFRelease(sec_transform)