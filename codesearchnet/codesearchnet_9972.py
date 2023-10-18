def load_public_key(source):
    """
    Loads a public key into a PublicKey object

    :param source:
        A byte string of file contents, a unicode string filename or an
        asn1crypto.keys.PublicKeyInfo object

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        oscrypto.errors.AsymmetricKeyError - when the public key is incompatible with the OS crypto library
        OSError - when an error is returned by the OS crypto library

    :return:
        A PublicKey object
    """

    if isinstance(source, keys.PublicKeyInfo):
        public_key = source

    elif isinstance(source, byte_cls):
        public_key = parse_public(source)

    elif isinstance(source, str_cls):
        with open(source, 'rb') as f:
            public_key = parse_public(f.read())

    else:
        raise TypeError(pretty_message(
            '''
            source must be a byte string, unicode string or
            asn1crypto.keys.PublicKeyInfo object, not %s
            ''',
            type_name(public_key)
        ))

    if public_key.algorithm == 'dsa':
        if libcrypto_version_info < (1,) and public_key.hash_algo == 'sha2':
            raise AsymmetricKeyError(pretty_message(
                '''
                OpenSSL 0.9.8 only supports DSA keys based on SHA1 (2048 bits or
                less) - this key is based on SHA2 and is %s bits
                ''',
                public_key.bit_size
            ))
        elif public_key.hash_algo is None:
            raise IncompleteAsymmetricKeyError(pretty_message(
                '''
                The DSA key does not contain the necessary p, q and g
                parameters and can not be used
                '''
            ))

    data = public_key.dump()
    buffer = buffer_from_bytes(data)
    evp_pkey = libcrypto.d2i_PUBKEY(null(), buffer_pointer(buffer), len(data))
    if is_null(evp_pkey):
        handle_openssl_error(0)
    return PublicKey(evp_pkey, public_key)