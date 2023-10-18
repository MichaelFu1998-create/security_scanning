def _advapi32_decrypt(cipher, key, data, iv, padding):
    """
    Decrypts AES/RC4/RC2/3DES/DES ciphertext via CryptoAPI

    :param cipher:
        A unicode string of "aes", "des", "tripledes_2key", "tripledes_3key",
        "rc2", "rc4"

    :param key:
        The encryption key - a byte string 5-16 bytes long

    :param data:
        The ciphertext - a byte string

    :param iv:
        The initialization vector - a byte string - unused for RC4

    :param padding:
        Boolean, if padding should be used - unused for RC4

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the plaintext
    """

    context_handle = None
    key_handle = None

    try:
        context_handle, key_handle = _advapi32_create_handles(cipher, key, iv)

        # Add removed padding when not required. CryptoAPI doesn't support no
        # padding, so we just add it back in
        if cipher == 'aes' and not padding:
            data += (b'\x10' * 16)

        buffer = buffer_from_bytes(data)
        out_len = new(advapi32, 'DWORD *', len(data))
        res = advapi32.CryptDecrypt(
            key_handle,
            null(),
            True,
            0,
            buffer,
            out_len
        )
        handle_error(res)

        return bytes_from_buffer(buffer, deref(out_len))

    finally:
        if key_handle:
            advapi32.CryptDestroyKey(key_handle)
        if context_handle:
            close_context_handle(context_handle)