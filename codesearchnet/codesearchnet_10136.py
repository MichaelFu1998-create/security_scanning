def _load_key(key_object):
    """
    Common code to load public and private keys into PublicKey and PrivateKey
    objects

    :param key_object:
        An asn1crypto.keys.PublicKeyInfo or asn1crypto.keys.PrivateKeyInfo
        object

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        oscrypto.errors.AsymmetricKeyError - when the key is incompatible with the OS crypto library
        OSError - when an error is returned by the OS crypto library

    :return:
        A PublicKey or PrivateKey object
    """

    if key_object.algorithm == 'ec':
        curve_type, details = key_object.curve
        if curve_type != 'named':
            raise AsymmetricKeyError('OS X only supports EC keys using named curves')
        if details not in set(['secp256r1', 'secp384r1', 'secp521r1']):
            raise AsymmetricKeyError(pretty_message(
                '''
                OS X only supports EC keys using the named curves secp256r1,
                secp384r1 and secp521r1
                '''
            ))

    elif key_object.algorithm == 'dsa' and key_object.hash_algo == 'sha2':
        raise AsymmetricKeyError(pretty_message(
            '''
            OS X only supports DSA keys based on SHA1 (2048 bits or less) - this
            key is based on SHA2 and is %s bits
            ''',
            key_object.bit_size
        ))

    elif key_object.algorithm == 'dsa' and key_object.hash_algo is None:
        raise IncompleteAsymmetricKeyError(pretty_message(
            '''
            The DSA key does not contain the necessary p, q and g parameters
            and can not be used
            '''
        ))

    if isinstance(key_object, keys.PublicKeyInfo):
        source = key_object.dump()
        key_class = Security.kSecAttrKeyClassPublic
    else:
        source = key_object.unwrap().dump()
        key_class = Security.kSecAttrKeyClassPrivate

    cf_source = None
    cf_dict = None
    cf_output = None

    try:
        cf_source = CFHelpers.cf_data_from_bytes(source)
        key_type = {
            'dsa': Security.kSecAttrKeyTypeDSA,
            'ec': Security.kSecAttrKeyTypeECDSA,
            'rsa': Security.kSecAttrKeyTypeRSA,
        }[key_object.algorithm]
        cf_dict = CFHelpers.cf_dictionary_from_pairs([
            (Security.kSecAttrKeyType, key_type),
            (Security.kSecAttrKeyClass, key_class),
            (Security.kSecAttrCanSign, CoreFoundation.kCFBooleanTrue),
            (Security.kSecAttrCanVerify, CoreFoundation.kCFBooleanTrue),
        ])
        error_pointer = new(CoreFoundation, 'CFErrorRef *')
        sec_key_ref = Security.SecKeyCreateFromData(cf_dict, cf_source, error_pointer)
        handle_cf_error(error_pointer)

        if key_class == Security.kSecAttrKeyClassPublic:
            return PublicKey(sec_key_ref, key_object)

        if key_class == Security.kSecAttrKeyClassPrivate:
            return PrivateKey(sec_key_ref, key_object)

    finally:
        if cf_source:
            CoreFoundation.CFRelease(cf_source)
        if cf_dict:
            CoreFoundation.CFRelease(cf_dict)
        if cf_output:
            CoreFoundation.CFRelease(cf_output)