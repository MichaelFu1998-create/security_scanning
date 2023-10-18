def _encrypt(cipher, key, data, iv, padding):
    """
    Encrypts plaintext

    :param cipher:
        A kSecAttrKeyType* value that specifies the cipher to use

    :param key:
        The encryption key - a byte string 5-16 bytes long

    :param data:
        The plaintext - a byte string

    :param iv:
        The initialization vector - a byte string - unused for RC4

    :param padding:
        The padding mode to use, specified as a kSecPadding*Key value - unused for RC4

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the ciphertext
    """

    if not isinstance(key, byte_cls):
        raise TypeError(pretty_message(
            '''
            key must be a byte string, not %s
            ''',
            type_name(key)
        ))

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    if cipher != Security.kSecAttrKeyTypeRC4 and not isinstance(iv, byte_cls):
        raise TypeError(pretty_message(
            '''
            iv must be a byte string, not %s
            ''',
            type_name(iv)
        ))

    if cipher != Security.kSecAttrKeyTypeRC4 and not padding:
        raise ValueError('padding must be specified')

    cf_dict = None
    cf_key = None
    cf_data = None
    cf_iv = None
    sec_key = None
    sec_transform = None

    try:
        cf_dict = CFHelpers.cf_dictionary_from_pairs([(Security.kSecAttrKeyType, cipher)])
        cf_key = CFHelpers.cf_data_from_bytes(key)
        cf_data = CFHelpers.cf_data_from_bytes(data)

        error_pointer = new(CoreFoundation, 'CFErrorRef *')
        sec_key = Security.SecKeyCreateFromData(cf_dict, cf_key, error_pointer)
        handle_cf_error(error_pointer)

        sec_transform = Security.SecEncryptTransformCreate(sec_key, error_pointer)
        handle_cf_error(error_pointer)

        if cipher != Security.kSecAttrKeyTypeRC4:
            Security.SecTransformSetAttribute(sec_transform, Security.kSecModeCBCKey, null(), error_pointer)
            handle_cf_error(error_pointer)

            Security.SecTransformSetAttribute(sec_transform, Security.kSecPaddingKey, padding, error_pointer)
            handle_cf_error(error_pointer)

            cf_iv = CFHelpers.cf_data_from_bytes(iv)
            Security.SecTransformSetAttribute(sec_transform, Security.kSecIVKey, cf_iv, error_pointer)
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
        if cf_dict:
            CoreFoundation.CFRelease(cf_dict)
        if cf_key:
            CoreFoundation.CFRelease(cf_key)
        if cf_data:
            CoreFoundation.CFRelease(cf_data)
        if cf_iv:
            CoreFoundation.CFRelease(cf_iv)
        if sec_key:
            CoreFoundation.CFRelease(sec_key)
        if sec_transform:
            CoreFoundation.CFRelease(sec_transform)