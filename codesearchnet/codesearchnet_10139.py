def _encrypt(certificate_or_public_key, data, padding):
    """
    Encrypts plaintext using an RSA public key or certificate

    :param certificate_or_public_key:
        A Certificate or PublicKey object

    :param data:
        The plaintext - a byte string

    :param padding:
        The padding mode to use, specified as a kSecPadding*Key value

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the ciphertext
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

    if not padding:
        raise ValueError('padding must be specified')

    cf_data = None
    sec_transform = None

    try:
        cf_data = CFHelpers.cf_data_from_bytes(data)

        error_pointer = new(CoreFoundation, 'CFErrorRef *')
        sec_transform = Security.SecEncryptTransformCreate(
            certificate_or_public_key.sec_key_ref,
            error_pointer
        )
        handle_cf_error(error_pointer)

        if padding:
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

        ciphertext = Security.SecTransformExecute(sec_transform, error_pointer)
        handle_cf_error(error_pointer)

        return CFHelpers.cf_data_to_bytes(ciphertext)

    finally:
        if cf_data:
            CoreFoundation.CFRelease(cf_data)
        if sec_transform:
            CoreFoundation.CFRelease(sec_transform)