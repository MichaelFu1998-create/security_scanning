def generate_pair(algorithm, bit_size=None, curve=None):
    """
    Generates a public/private key pair

    :param algorithm:
        The key algorithm - "rsa", "dsa" or "ec"

    :param bit_size:
        An integer - used for "rsa" and "dsa". For "rsa" the value maye be 1024,
        2048, 3072 or 4096. For "dsa" the value may be 1024.

    :param curve:
        A unicode string - used for "ec" keys. Valid values include "secp256r1",
        "secp384r1" and "secp521r1".

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A 2-element tuple of (PublicKey, PrivateKey). The contents of each key
        may be saved by calling .asn1.dump().
    """

    if algorithm not in set(['rsa', 'dsa', 'ec']):
        raise ValueError(pretty_message(
            '''
            algorithm must be one of "rsa", "dsa", "ec", not %s
            ''',
            repr(algorithm)
        ))

    if algorithm == 'rsa':
        if bit_size not in set([1024, 2048, 3072, 4096]):
            raise ValueError(pretty_message(
                '''
                bit_size must be one of 1024, 2048, 3072, 4096, not %s
                ''',
                repr(bit_size)
            ))

    elif algorithm == 'dsa':
        if bit_size not in set([1024]):
            raise ValueError(pretty_message(
                '''
                bit_size must be 1024, not %s
                ''',
                repr(bit_size)
            ))

    elif algorithm == 'ec':
        if curve not in set(['secp256r1', 'secp384r1', 'secp521r1']):
            raise ValueError(pretty_message(
                '''
                curve must be one of "secp256r1", "secp384r1", "secp521r1", not %s
                ''',
                repr(curve)
            ))

    cf_dict = None
    public_key_ref = None
    private_key_ref = None
    cf_data_public = None
    cf_data_private = None
    cf_string = None
    sec_access_ref = None

    try:
        key_type = {
            'dsa': Security.kSecAttrKeyTypeDSA,
            'ec': Security.kSecAttrKeyTypeECDSA,
            'rsa': Security.kSecAttrKeyTypeRSA,
        }[algorithm]

        if algorithm == 'ec':
            key_size = {
                'secp256r1': 256,
                'secp384r1': 384,
                'secp521r1': 521,
            }[curve]
        else:
            key_size = bit_size

        private_key_pointer = new(Security, 'SecKeyRef *')
        public_key_pointer = new(Security, 'SecKeyRef *')

        cf_string = CFHelpers.cf_string_from_unicode("Temporary key from oscrypto python library - safe to delete")

        # For some reason Apple decided that DSA keys were not a valid type of
        # key to be generated via SecKeyGeneratePair(), thus we have to use the
        # lower level, deprecated SecKeyCreatePair()
        if algorithm == 'dsa':
            sec_access_ref_pointer = new(Security, 'SecAccessRef *')
            result = Security.SecAccessCreate(cf_string, null(), sec_access_ref_pointer)
            sec_access_ref = unwrap(sec_access_ref_pointer)

            result = Security.SecKeyCreatePair(
                null(),
                SecurityConst.CSSM_ALGID_DSA,
                key_size,
                0,
                SecurityConst.CSSM_KEYUSE_VERIFY,
                SecurityConst.CSSM_KEYATTR_EXTRACTABLE | SecurityConst.CSSM_KEYATTR_PERMANENT,
                SecurityConst.CSSM_KEYUSE_SIGN,
                SecurityConst.CSSM_KEYATTR_EXTRACTABLE | SecurityConst.CSSM_KEYATTR_PERMANENT,
                sec_access_ref,
                public_key_pointer,
                private_key_pointer
            )
            handle_sec_error(result)
        else:
            cf_dict = CFHelpers.cf_dictionary_from_pairs([
                (Security.kSecAttrKeyType, key_type),
                (Security.kSecAttrKeySizeInBits, CFHelpers.cf_number_from_integer(key_size)),
                (Security.kSecAttrLabel, cf_string)
            ])
            result = Security.SecKeyGeneratePair(cf_dict, public_key_pointer, private_key_pointer)
            handle_sec_error(result)

        public_key_ref = unwrap(public_key_pointer)
        private_key_ref = unwrap(private_key_pointer)

        cf_data_public_pointer = new(CoreFoundation, 'CFDataRef *')
        result = Security.SecItemExport(public_key_ref, 0, 0, null(), cf_data_public_pointer)
        handle_sec_error(result)
        cf_data_public = unwrap(cf_data_public_pointer)
        public_key_bytes = CFHelpers.cf_data_to_bytes(cf_data_public)

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

    finally:
        if cf_dict:
            CoreFoundation.CFRelease(cf_dict)
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

    return (load_public_key(public_key_bytes), load_private_key(private_key_bytes))