def _bcrypt_encrypt(cipher, key, data, iv, padding):
    """
    Encrypts plaintext via CNG

    :param cipher:
        A unicode string of "aes", "des", "tripledes_2key", "tripledes_3key",
        "rc2", "rc4"

    :param key:
        The encryption key - a byte string 5-16 bytes long

    :param data:
        The plaintext - a byte string

    :param iv:
        The initialization vector - a byte string - unused for RC4

    :param padding:
        Boolean, if padding should be used - unused for RC4

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the ciphertext
    """

    key_handle = None

    try:
        key_handle = _bcrypt_create_key_handle(cipher, key)

        if iv is None:
            iv_len = 0
        else:
            iv_len = len(iv)

        flags = 0
        if padding is True:
            flags = BcryptConst.BCRYPT_BLOCK_PADDING

        out_len = new(bcrypt, 'ULONG *')
        res = bcrypt.BCryptEncrypt(
            key_handle,
            data,
            len(data),
            null(),
            null(),
            0,
            null(),
            0,
            out_len,
            flags
        )
        handle_error(res)

        buffer_len = deref(out_len)
        buffer = buffer_from_bytes(buffer_len)
        iv_buffer = buffer_from_bytes(iv) if iv else null()

        res = bcrypt.BCryptEncrypt(
            key_handle,
            data,
            len(data),
            null(),
            iv_buffer,
            iv_len,
            buffer,
            buffer_len,
            out_len,
            flags
        )
        handle_error(res)

        return bytes_from_buffer(buffer, deref(out_len))

    finally:
        if key_handle:
            bcrypt.BCryptDestroyKey(key_handle)