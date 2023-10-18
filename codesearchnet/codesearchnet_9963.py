def _encrypt(cipher, key, data, iv, padding):
    """
    Encrypts plaintext

    :param cipher:
        A unicode string of "aes128", "aes192", "aes256", "des",
        "tripledes_2key", "tripledes_3key", "rc2", "rc4"

    :param key:
        The encryption key - a byte string 5-32 bytes long

    :param data:
        The plaintext - a byte string

    :param iv:
        The initialization vector - a byte string - unused for RC4

    :param padding:
        Boolean, if padding should be used - unused for RC4

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by OpenSSL

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

    if cipher != 'rc4' and not isinstance(iv, byte_cls):
        raise TypeError(pretty_message(
            '''
            iv must be a byte string, not %s
            ''',
            type_name(iv)
        ))

    if cipher != 'rc4' and not padding:
        raise ValueError('padding must be specified')

    evp_cipher_ctx = None

    try:
        evp_cipher_ctx = libcrypto.EVP_CIPHER_CTX_new()
        if is_null(evp_cipher_ctx):
            handle_openssl_error(0)

        evp_cipher, buffer_size = _setup_evp_encrypt_decrypt(cipher, data)

        if iv is None:
            iv = null()

        if cipher in set(['rc2', 'rc4']):
            res = libcrypto.EVP_EncryptInit_ex(evp_cipher_ctx, evp_cipher, null(), null(), null())
            handle_openssl_error(res)
            res = libcrypto.EVP_CIPHER_CTX_set_key_length(evp_cipher_ctx, len(key))
            handle_openssl_error(res)
            if cipher == 'rc2':
                res = libcrypto.EVP_CIPHER_CTX_ctrl(
                    evp_cipher_ctx,
                    LibcryptoConst.EVP_CTRL_SET_RC2_KEY_BITS,
                    len(key) * 8,
                    null()
                )
                handle_openssl_error(res)
            evp_cipher = null()

        res = libcrypto.EVP_EncryptInit_ex(evp_cipher_ctx, evp_cipher, null(), key, iv)
        handle_openssl_error(res)

        if padding is not None:
            res = libcrypto.EVP_CIPHER_CTX_set_padding(evp_cipher_ctx, int(padding))
            handle_openssl_error(res)

        buffer = buffer_from_bytes(buffer_size)
        output_length = new(libcrypto, 'int *')

        res = libcrypto.EVP_EncryptUpdate(evp_cipher_ctx, buffer, output_length, data, len(data))
        handle_openssl_error(res)

        output = bytes_from_buffer(buffer, deref(output_length))

        res = libcrypto.EVP_EncryptFinal_ex(evp_cipher_ctx, buffer, output_length)
        handle_openssl_error(res)

        output += bytes_from_buffer(buffer, deref(output_length))

        return output

    finally:
        if evp_cipher_ctx:
            libcrypto.EVP_CIPHER_CTX_free(evp_cipher_ctx)