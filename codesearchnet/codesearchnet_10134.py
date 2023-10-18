def generate_dh_parameters(bit_size):
    """
    Generates DH parameters for use with Diffie-Hellman key exchange. Returns
    a structure in the format of DHParameter defined in PKCS#3, which is also
    used by the OpenSSL dhparam tool.

    THIS CAN BE VERY TIME CONSUMING!

    :param bit_size:
        The integer bit size of the parameters to generate. Must be between 512
        and 4096, and divisible by 64. Recommended secure value as of early 2016
        is 2048, with an absolute minimum of 1024.

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        An asn1crypto.algos.DHParameters object. Use
        oscrypto.asymmetric.dump_dh_parameters() to save to disk for usage with
        web servers.
    """

    if not isinstance(bit_size, int_types):
        raise TypeError(pretty_message(
            '''
            bit_size must be an integer, not %s
            ''',
            type_name(bit_size)
        ))

    if bit_size < 512:
        raise ValueError('bit_size must be greater than or equal to 512')

    if bit_size > 4096:
        raise ValueError('bit_size must be less than or equal to 4096')

    if bit_size % 64 != 0:
        raise ValueError('bit_size must be a multiple of 64')

    public_key_ref = None
    private_key_ref = None
    cf_data_public = None
    cf_data_private = None
    cf_string = None
    sec_access_ref = None

    try:
        public_key_pointer = new(Security, 'SecKeyRef *')
        private_key_pointer = new(Security, 'SecKeyRef *')

        cf_string = CFHelpers.cf_string_from_unicode("Temporary key from oscrypto python library - safe to delete")

        sec_access_ref_pointer = new(Security, 'SecAccessRef *')
        result = Security.SecAccessCreate(cf_string, null(), sec_access_ref_pointer)
        sec_access_ref = unwrap(sec_access_ref_pointer)

        result = Security.SecKeyCreatePair(
            null(),
            SecurityConst.CSSM_ALGID_DH,
            bit_size,
            0,
            0,
            SecurityConst.CSSM_KEYATTR_EXTRACTABLE | SecurityConst.CSSM_KEYATTR_PERMANENT,
            0,
            SecurityConst.CSSM_KEYATTR_EXTRACTABLE | SecurityConst.CSSM_KEYATTR_PERMANENT,
            sec_access_ref,
            public_key_pointer,
            private_key_pointer
        )
        handle_sec_error(result)

        public_key_ref = unwrap(public_key_pointer)
        private_key_ref = unwrap(private_key_pointer)

        cf_data_private_pointer = new(CoreFoundation, 'CFDataRef *')
        result = Security.SecItemExport(private_key_ref, 0, 0, null(), cf_data_private_pointer)
        handle_sec_error(result)
        cf_data_private = unwrap(cf_data_private_pointer)
        private_key_bytes = CFHelpers.cf_data_to_bytes(cf_data_private)

        # Clean the new keys out of the keychain
        result = Security.SecKeychainItemDelete(public_key_ref)
        handle_sec_error(result)

        result = Security.SecKeychainItemDelete(private_key_ref)
        handle_sec_error(result)

        return algos.KeyExchangeAlgorithm.load(private_key_bytes)['parameters']

    finally:
        if public_key_ref:
            CoreFoundation.CFRelease(public_key_ref)
        if private_key_ref:
            CoreFoundation.CFRelease(private_key_ref)
        if cf_data_public:
            CoreFoundation.CFRelease(cf_data_public)
        if cf_data_private:
            CoreFoundation.CFRelease(cf_data_private)
        if cf_string:
            CoreFoundation.CFRelease(cf_string)
        if sec_access_ref:
            CoreFoundation.CFRelease(sec_access_ref)