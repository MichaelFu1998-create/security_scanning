def _verify(certificate_or_public_key, signature, data, hash_algorithm, rsa_pss_padding=False):
    """
    Verifies an RSA, DSA or ECDSA signature

    :param certificate_or_public_key:
        A Certificate or PublicKey instance to verify the signature with

    :param signature:
        A byte string of the signature to verify

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha224", "sha256", "sha384" or "sha512"

    :param rsa_pss_padding:
        If the certificate_or_public_key is an RSA key, this enables PSS padding

    :raises:
        oscrypto.errors.SignatureError - when the signature is determined to be invalid
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library
    """

    if not isinstance(certificate_or_public_key, (Certificate, PublicKey)):
        raise TypeError(pretty_message(
            '''
            certificate_or_public_key must be an instance of the Certificate or
            PublicKey class, not %s
            ''',
            type_name(certificate_or_public_key)
        ))

    if not isinstance(signature, byte_cls):
        raise TypeError(pretty_message(
            '''
            signature must be a byte string, not %s
            ''',
            type_name(signature)
        ))

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    valid_hash_algorithms = set(['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512'])
    if certificate_or_public_key.algorithm == 'rsa' and not rsa_pss_padding:
        valid_hash_algorithms |= set(['raw'])

    if hash_algorithm not in valid_hash_algorithms:
        valid_hash_algorithms_error = '"md5", "sha1", "sha224", "sha256", "sha384", "sha512"'
        if certificate_or_public_key.algorithm == 'rsa' and not rsa_pss_padding:
            valid_hash_algorithms_error += ', "raw"'
        raise ValueError(pretty_message(
            '''
            hash_algorithm must be one of %s, not %s
            ''',
            valid_hash_algorithms_error,
            repr(hash_algorithm)
        ))

    if certificate_or_public_key.algorithm != 'rsa' and rsa_pss_padding:
        raise ValueError(pretty_message(
            '''
            PSS padding can only be used with RSA keys - the key provided is a
            %s key
            ''',
            certificate_or_public_key.algorithm.upper()
        ))

    if certificate_or_public_key.algorithm == 'rsa' and hash_algorithm == 'raw':
        if len(data) > certificate_or_public_key.byte_size - 11:
            raise ValueError(pretty_message(
                '''
                data must be 11 bytes shorter than the key size when
                hash_algorithm is "raw" - key size is %s bytes, but data is
                %s bytes long
                ''',
                certificate_or_public_key.byte_size,
                len(data)
            ))

        rsa = None

        try:
            rsa = libcrypto.EVP_PKEY_get1_RSA(certificate_or_public_key.evp_pkey)
            if is_null(rsa):
                handle_openssl_error(0)

            buffer_size = libcrypto.EVP_PKEY_size(certificate_or_public_key.evp_pkey)
            decrypted_buffer = buffer_from_bytes(buffer_size)
            decrypted_length = libcrypto.RSA_public_decrypt(
                len(signature),
                signature,
                decrypted_buffer,
                rsa,
                LibcryptoConst.RSA_PKCS1_PADDING
            )
            handle_openssl_error(decrypted_length)

            decrypted_bytes = bytes_from_buffer(decrypted_buffer, decrypted_length)

            if not constant_compare(data, decrypted_bytes):
                raise SignatureError('Signature is invalid')
            return

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
            if certificate_or_public_key.algorithm == 'rsa' and rsa_pss_padding:
                digest = getattr(hashlib, hash_algorithm)(data).digest()

                rsa = libcrypto.EVP_PKEY_get1_RSA(certificate_or_public_key.evp_pkey)
                if is_null(rsa):
                    handle_openssl_error(0)

                buffer_size = libcrypto.EVP_PKEY_size(certificate_or_public_key.evp_pkey)
                decoded_buffer = buffer_from_bytes(buffer_size)
                decoded_length = libcrypto.RSA_public_decrypt(
                    len(signature),
                    signature,
                    decoded_buffer,
                    rsa,
                    LibcryptoConst.RSA_NO_PADDING
                )
                handle_openssl_error(decoded_length)

                res = libcrypto.RSA_verify_PKCS1_PSS(
                    rsa,
                    digest,
                    evp_md,
                    decoded_buffer,
                    LibcryptoConst.EVP_MD_CTX_FLAG_PSS_MDLEN
                )

            elif certificate_or_public_key.algorithm == 'rsa':
                res = libcrypto.EVP_DigestInit_ex(evp_md_ctx, evp_md, null())
                handle_openssl_error(res)

                res = libcrypto.EVP_DigestUpdate(evp_md_ctx, data, len(data))
                handle_openssl_error(res)

                res = libcrypto.EVP_VerifyFinal(
                    evp_md_ctx,
                    signature,
                    len(signature),
                    certificate_or_public_key.evp_pkey
                )

            elif certificate_or_public_key.algorithm == 'dsa':
                digest = getattr(hashlib, hash_algorithm)(data).digest()

                signature_buffer = buffer_from_bytes(signature)
                signature_pointer = buffer_pointer(signature_buffer)
                dsa_sig = libcrypto.d2i_DSA_SIG(null(), signature_pointer, len(signature))
                if is_null(dsa_sig):
                    raise SignatureError('Signature is invalid')

                dsa = libcrypto.EVP_PKEY_get1_DSA(certificate_or_public_key.evp_pkey)
                if is_null(dsa):
                    handle_openssl_error(0)

                res = libcrypto.DSA_do_verify(digest, len(digest), dsa_sig, dsa)

            elif certificate_or_public_key.algorithm == 'ec':
                digest = getattr(hashlib, hash_algorithm)(data).digest()

                signature_buffer = buffer_from_bytes(signature)
                signature_pointer = buffer_pointer(signature_buffer)
                ecdsa_sig = libcrypto.d2i_ECDSA_SIG(null(), signature_pointer, len(signature))
                if is_null(ecdsa_sig):
                    raise SignatureError('Signature is invalid')

                ec_key = libcrypto.EVP_PKEY_get1_EC_KEY(certificate_or_public_key.evp_pkey)
                if is_null(ec_key):
                    handle_openssl_error(0)

                res = libcrypto.ECDSA_do_verify(digest, len(digest), ecdsa_sig, ec_key)

        else:
            evp_pkey_ctx_pointer_pointer = new(libcrypto, 'EVP_PKEY_CTX **')
            res = libcrypto.EVP_DigestVerifyInit(
                evp_md_ctx,
                evp_pkey_ctx_pointer_pointer,
                evp_md,
                null(),
                certificate_or_public_key.evp_pkey
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

            res = libcrypto.EVP_DigestVerifyFinal(evp_md_ctx, signature, len(signature))

        if res < 1:
            raise SignatureError('Signature is invalid')
        handle_openssl_error(res)

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