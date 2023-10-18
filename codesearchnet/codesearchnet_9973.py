def _load_key(private_object):
    """
    Loads a private key into a PrivateKey object

    :param private_object:
        An asn1crypto.keys.PrivateKeyInfo object

    :return:
        A PrivateKey object
    """

    if libcrypto_version_info < (1,) and private_object.algorithm == 'dsa' and private_object.hash_algo == 'sha2':
        raise AsymmetricKeyError(pretty_message(
            '''
            OpenSSL 0.9.8 only supports DSA keys based on SHA1 (2048 bits or
            less) - this key is based on SHA2 and is %s bits
            ''',
            private_object.bit_size
        ))

    source = private_object.unwrap().dump()

    buffer = buffer_from_bytes(source)
    evp_pkey = libcrypto.d2i_AutoPrivateKey(null(), buffer_pointer(buffer), len(source))
    if is_null(evp_pkey):
        handle_openssl_error(0)
    return PrivateKey(evp_pkey, private_object)