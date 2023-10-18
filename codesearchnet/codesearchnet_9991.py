def _advapi32_load_key(key_object, key_info, container):
    """
    Loads a certificate, public key or private key into a Certificate,
    PublicKey or PrivateKey object via CryptoAPI

    :param key_object:
        An asn1crypto.x509.Certificate, asn1crypto.keys.PublicKeyInfo or
        asn1crypto.keys.PrivateKeyInfo object

    :param key_info:
        An asn1crypto.keys.PublicKeyInfo or asn1crypto.keys.PrivateKeyInfo
        object

    :param container:
        The class of the object to hold the key_handle

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        oscrypto.errors.AsymmetricKeyError - when the key is incompatible with the OS crypto library
        OSError - when an error is returned by the OS crypto library

    :return:
        A PrivateKey, PublicKey or Certificate object, based on container
    """

    key_type = 'public' if isinstance(key_info, keys.PublicKeyInfo) else 'private'
    algo = key_info.algorithm

    if algo == 'rsa':
        provider = Advapi32Const.MS_ENH_RSA_AES_PROV
    else:
        provider = Advapi32Const.MS_ENH_DSS_DH_PROV

    context_handle = None
    key_handle = None

    try:
        context_handle = open_context_handle(provider, verify_only=key_type == 'public')

        blob = _advapi32_create_blob(key_info, key_type, algo)
        buffer_ = buffer_from_bytes(blob)

        key_handle_pointer = new(advapi32, 'HCRYPTKEY *')
        res = advapi32.CryptImportKey(
            context_handle,
            buffer_,
            len(blob),
            null(),
            0,
            key_handle_pointer
        )
        handle_error(res)

        key_handle = unwrap(key_handle_pointer)
        output = container(key_handle, key_object)
        output.context_handle = context_handle

        if algo == 'rsa':
            ex_blob = _advapi32_create_blob(key_info, key_type, algo, signing=False)
            ex_buffer = buffer_from_bytes(ex_blob)

            ex_key_handle_pointer = new(advapi32, 'HCRYPTKEY *')
            res = advapi32.CryptImportKey(
                context_handle,
                ex_buffer,
                len(ex_blob),
                null(),
                0,
                ex_key_handle_pointer
            )
            handle_error(res)

            output.ex_key_handle = unwrap(ex_key_handle_pointer)

        return output

    except (Exception):
        if key_handle:
            advapi32.CryptDestroyKey(key_handle)
        if context_handle:
            close_context_handle(context_handle)
        raise