def _sign(private_key, data, hash_algorithm, rsa_pss_padding=False):
    """
    Generates an RSA, DSA or ECDSA signature

    :param private_key:
        The PrivateKey to generate the signature with

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha224", "sha256", "sha384" or "sha512"

    :param rsa_pss_padding:
        If the private_key is an RSA key, this enables PSS padding

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the signature
    """

    if not isinstance(private_key, PrivateKey):
        raise TypeError(pretty_message(
            '''
            private_key must be an instance of PrivateKey, not %s
            ''',
            type_name(private_key)
        ))

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    valid_hash_algorithms = set(['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'])
    if private_key.algorithm == 'rsa' and not rsa_pss_padding:
        valid_hash_algorithms |= set(['raw'])

    if hash_algorithm not in valid_hash_algorithms:
        valid_hash_algorithms_error = '"md5", "sha1", "sha224", "sha256", "sha384", "sha512"'
        if private_key.algorithm == 'rsa' and not rsa_pss_padding:
            valid_hash_algorithms_error += ', "raw"'
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of %s, not %s
            ''',
            valid_hash_algorithms_error,
            repr(hash_algorithm)
        ))

    if private_key.algorithm != 'rsa' and rsa_pss_padding:
        raise ValueError(pretty_message(
            '''
            PSS padding can only be used with RSA keys - the key provided is a
            %s key
            ''',
            private_key.algorithm.upper()
        ))

    if private_key.algorithm == 'rsa' and hash_algorithm == 'raw':
        if len(data) > private_key.byte_size - 11:
            raise ValueError(pretty_message(
                '''
                data must be 11 bytes shorter than the key size when
                hash_algorithm is "raw" - key size is %s bytes, but data is
                %s bytes long
                ''',
                private_key.byte_size,
                len(data)
            ))

        rsa = None

        try:
            rsa = libcrypto.EVP_PKEY_get1_RSA(private_key.evp_pkey)
            if is_null(rsa):
                handle_openssl_error(0)

            buffer_size = libcrypto.EVP_PKEY_size(private_key.evp_pkey)

            signature_buffer = buffer_from_bytes(buffer_size)
            signature_length = libcrypto.RSA_private_encrypt(
                len(data),
                data,
                signature_buffer,
                rsa,
                LibcryptoConst.RSA_PKCS1_PADDING
            )
            handle_openssl_error(signature_length)

            return bytes_from_buffer(signature_buffer, signature_length)

        finally:
            if rsa:
                libcrypto.RSA_free(rsa)

    evp_md_ctx = None
    rsa = None
    dsa = None
    dsa_sig = None
    ec_key = None
    ecdsa_sig = None

    try:
        if libcrypto_version_info < (1, 1):
            evp_md_ctx = libcrypto.EVP_MD_CTX_create()
        else:
            evp_md_ctx = libcrypto.EVP_MD_CTX_new()

        evp_md = {
            'md5': libcrypto.EVP_md5,
            'sha1': libcrypto.EVP_sha1,
            'sha224': libcrypto.EVP_sha224,
            'sha256': libcrypto.EVP_sha256,
            'sha384': libcrypto.EVP_sha384,
            'sha512': libcrypto.EVP_sha512
        }[hash_algorithm]()

        if libcrypto_version_info < (1,):
            if private_key.algorithm == 'rsa' and rsa_pss_padding:
                digest = getattr(hashlib, hash_algorithm)(data).digest()

                rsa = libcrypto.EVP_PKEY_get1_RSA(private_key.evp_pkey)
                if is_null(rsa):
                    handle_openssl_error(0)

                buffer_size = libcrypto.EVP_PKEY_size(private_key.evp_pkey)
                em_buffer = buffer_from_bytes(buffer_size)
                res = libcrypto.RSA_padding_add_PKCS1_PSS(
                    rsa,
                    em_buffer,
                    digest,
                    evp_md,
                    LibcryptoConst.EVP_MD_CTX_FLAG_PSS_MDLEN
                )
                handle_openssl_error(res)

                signature_buffer = buffer_from_bytes(buffer_size)
                signature_length = libcrypto.RSA_private_encrypt(
                    buffer_size,
                    em_buffer,
                    signature_buffer,
                    rsa,
                    LibcryptoConst.RSA_NO_PADDING
                )
                handle_openssl_error(signature_length)

            elif private_key.algorithm == 'rsa':
                buffer_size = libcrypto.EVP_PKEY_size(private_key.evp_pkey)
                signature_buffer = buffer_from_bytes(buffer_size)
                signature_length = new(libcrypto, 'unsigned int *')

                res = libcrypto.EVP_DigestInit_ex(evp_md_ctx, evp_md, null())
                handle_openssl_error(res)

                res = libcrypto.EVP_DigestUpdate(evp_md_ctx, data, len(data))
                handle_openssl_error(res)

                res = libcrypto.EVP_SignFinal(
                    evp_md_ctx,
                    signature_buffer,
                    signature_length,
                    private_key.evp_pkey
                )
                handle_openssl_error(res)

                signature_length = deref(signature_length)

            elif private_key.algorithm == 'dsa':
                digest = getattr(hashlib, hash_algorithm)(data).digest()

                dsa = libcrypto.EVP_PKEY_get1_DSA(private_key.evp_pkey)
                if is_null(dsa):
                    handle_openssl_error(0)

                dsa_sig = libcrypto.DSA_do_sign(digest, len(digest), dsa)
                if is_null(dsa_sig):
                    handle_openssl_error(0)

                buffer_size = libcrypto.i2d_DSA_SIG(dsa_sig, null())
                signature_buffer = buffer_from_bytes(buffer_size)
                signature_pointer = buffer_pointer(signature_buffer)
                signature_length = libcrypto.i2d_DSA_SIG(dsa_sig, signature_pointer)
                handle_openssl_error(signature_length)

            elif private_key.algorithm == 'ec':
                digest = getattr(hashlib, hash_algorithm)(data).digest()

                ec_key = libcrypto.EVP_PKEY_get1_EC_KEY(private_key.evp_pkey)
                if is_null(ec_key):
                    handle_openssl_error(0)

                ecdsa_sig = libcrypto.ECDSA_do_sign(digest, len(digest), ec_key)
                if is_null(ecdsa_sig):
                    handle_openssl_error(0)

                buffer_size = libcrypto.i2d_ECDSA_SIG(ecdsa_sig, null())
                signature_buffer = buffer_from_bytes(buffer_size)
                signature_pointer = buffer_pointer(signature_buffer)
                signature_length = libcrypto.i2d_ECDSA_SIG(ecdsa_sig, signature_pointer)
                handle_openssl_error(signature_length)

        else:
            buffer_size = libcrypto.EVP_PKEY_size(private_key.evp_pkey)
            signature_buffer = buffer_from_bytes(buffer_size)
            signature_length = new(libcrypto, 'size_t *', buffer_size)

            evp_pkey_ctx_pointer_pointer = new(libcrypto, 'EVP_PKEY_CTX **')
            res = libcrypto.EVP_DigestSignInit(
                evp_md_ctx,
                evp_pkey_ctx_pointer_pointer,
                evp_md,
                null(),
                private_key.evp_pkey
            )
            handle_openssl_error(res)
            evp_pkey_ctx_pointer = unwrap(evp_pkey_ctx_pointer_pointer)

            if rsa_pss_padding:
                # Enable PSS padding
                res = libcrypto.EVP_PKEY_CTX_ctrl(
                    evp_pkey_ctx_pointer,
                    LibcryptoConst.EVP_PKEY_RSA,
                    -1,  # All operations
                    LibcryptoConst.EVP_PKEY_CTRL_RSA_PADDING,
                    LibcryptoConst.RSA_PKCS1_PSS_PADDING,
                    null()
                )
                handle_openssl_error(res)

                # Use the hash algorithm output length as the salt length
                res = libcrypto.EVP_PKEY_CTX_ctrl(
                    evp_pkey_ctx_pointer,
                    LibcryptoConst.EVP_PKEY_RSA,
                    LibcryptoConst.EVP_PKEY_OP_SIGN | LibcryptoConst.EVP_PKEY_OP_VERIFY,
                    LibcryptoConst.EVP_PKEY_CTRL_RSA_PSS_SALTLEN,
                    -1,
                    null()
                )
                handle_openssl_error(res)

            res = libcrypto.EVP_DigestUpdate(evp_md_ctx, data, len(data))
            handle_openssl_error(res)

            res = libcrypto.EVP_DigestSignFinal(evp_md_ctx, signature_buffer, signature_length)
            handle_openssl_error(res)

            signature_length = deref(signature_length)

        return bytes_from_buffer(signature_buffer, signature_length)

    finally:
        if evp_md_ctx:
            if libcrypto_version_info < (1, 1):
                libcrypto.EVP_MD_CTX_destroy(evp_md_ctx)
            else:
                libcrypto.EVP_MD_CTX_free(evp_md_ctx)
        if rsa:
            libcrypto.RSA_free(rsa)
        if dsa:
            libcrypto.DSA_free(dsa)
        if dsa_sig:
            libcrypto.DSA_SIG_free(dsa_sig)
        if ec_key:
            libcrypto.EC_KEY_free(ec_key)
        if ecdsa_sig:
            libcrypto.ECDSA_SIG_free(ecdsa_sig)