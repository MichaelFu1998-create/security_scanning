def _advapi32_generate_pair(algorithm, bit_size=None):
    """
    Generates a public/private key pair using CryptoAPI

    :param algorithm:
        The key algorithm - "rsa" or "dsa"

    :param bit_size:
        An integer - used for "rsa" and "dsa". For "rsa" the value maye be 1024,
        2048, 3072 or 4096. For "dsa" the value may be 1024.

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A 2-element tuple of (PublicKey, PrivateKey). The contents of each key
        may be saved by calling .asn1.dump().
    """

    if algorithm == 'rsa':
        provider = Advapi32Const.MS_ENH_RSA_AES_PROV
        algorithm_id = Advapi32Const.CALG_RSA_SIGN
        struct_type = 'RSABLOBHEADER'
    else:
        provider = Advapi32Const.MS_ENH_DSS_DH_PROV
        algorithm_id = Advapi32Const.CALG_DSS_SIGN
        struct_type = 'DSSBLOBHEADER'

    context_handle = None
    key_handle = None

    try:
        context_handle = open_context_handle(provider, verify_only=False)

        key_handle_pointer = new(advapi32, 'HCRYPTKEY *')
        flags = (bit_size << 16) | Advapi32Const.CRYPT_EXPORTABLE
        res = advapi32.CryptGenKey(context_handle, algorithm_id, flags, key_handle_pointer)
        handle_error(res)

        key_handle = unwrap(key_handle_pointer)

        out_len = new(advapi32, 'DWORD *')
        res = advapi32.CryptExportKey(
            key_handle,
            null(),
            Advapi32Const.PRIVATEKEYBLOB,
            0,
            null(),
            out_len
        )
        handle_error(res)

        buffer_length = deref(out_len)
        buffer_ = buffer_from_bytes(buffer_length)
        res = advapi32.CryptExportKey(
            key_handle,
            null(),
            Advapi32Const.PRIVATEKEYBLOB,
            0,
            buffer_,
            out_len
        )
        handle_error(res)

        blob_struct_pointer = struct_from_buffer(advapi32, struct_type, buffer_)
        blob_struct = unwrap(blob_struct_pointer)
        struct_size = sizeof(advapi32, blob_struct)

        private_blob = bytes_from_buffer(buffer_, buffer_length)[struct_size:]

        if algorithm == 'rsa':
            public_info, private_info = _advapi32_interpret_rsa_key_blob(bit_size, blob_struct, private_blob)

        else:
            # The public key for a DSA key is not available in from the private
            # key blob, so we have to separately export the public key
            public_out_len = new(advapi32, 'DWORD *')
            res = advapi32.CryptExportKey(
                key_handle,
                null(),
                Advapi32Const.PUBLICKEYBLOB,
                0,
                null(),
                public_out_len
            )
            handle_error(res)

            public_buffer_length = deref(public_out_len)
            public_buffer = buffer_from_bytes(public_buffer_length)
            res = advapi32.CryptExportKey(
                key_handle,
                null(),
                Advapi32Const.PUBLICKEYBLOB,
                0,
                public_buffer,
                public_out_len
            )
            handle_error(res)

            public_blob = bytes_from_buffer(public_buffer, public_buffer_length)[struct_size:]

            public_info, private_info = _advapi32_interpret_dsa_key_blob(bit_size, public_blob, private_blob)

        return (load_public_key(public_info), load_private_key(private_info))

    finally:
        if context_handle:
            close_context_handle(context_handle)
        if key_handle:
            advapi32.CryptDestroyKey(key_handle)