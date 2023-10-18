def _bcrypt_create_key_handle(cipher, key):
    """
    Creates a BCRYPT_KEY_HANDLE for symmetric encryption/decryption. The
    handle must be released by bcrypt.BCryptDestroyKey() when done.

    :param cipher:
        A unicode string of "aes", "des", "tripledes_2key", "tripledes_3key",
        "rc2", "rc4"

    :param key:
        A byte string of the symmetric key

    :return:
        A BCRYPT_KEY_HANDLE
    """

    alg_handle = None

    alg_constant = {
        'aes': BcryptConst.BCRYPT_AES_ALGORITHM,
        'des': BcryptConst.BCRYPT_DES_ALGORITHM,
        'tripledes_2key': BcryptConst.BCRYPT_3DES_112_ALGORITHM,
        'tripledes_3key': BcryptConst.BCRYPT_3DES_ALGORITHM,
        'rc2': BcryptConst.BCRYPT_RC2_ALGORITHM,
        'rc4': BcryptConst.BCRYPT_RC4_ALGORITHM,
    }[cipher]

    try:
        alg_handle = open_alg_handle(alg_constant)
        blob_type = BcryptConst.BCRYPT_KEY_DATA_BLOB

        blob_struct_pointer = struct(bcrypt, 'BCRYPT_KEY_DATA_BLOB_HEADER')
        blob_struct = unwrap(blob_struct_pointer)
        blob_struct.dwMagic = BcryptConst.BCRYPT_KEY_DATA_BLOB_MAGIC
        blob_struct.dwVersion = BcryptConst.BCRYPT_KEY_DATA_BLOB_VERSION1
        blob_struct.cbKeyData = len(key)

        blob = struct_bytes(blob_struct_pointer) + key

        if cipher == 'rc2':
            buf = new(bcrypt, 'DWORD *', len(key) * 8)
            res = bcrypt.BCryptSetProperty(
                alg_handle,
                BcryptConst.BCRYPT_EFFECTIVE_KEY_LENGTH,
                buf,
                4,
                0
            )
            handle_error(res)

        key_handle_pointer = new(bcrypt, 'BCRYPT_KEY_HANDLE *')
        res = bcrypt.BCryptImportKey(
            alg_handle,
            null(),
            blob_type,
            key_handle_pointer,
            null(),
            0,
            blob,
            len(blob),
            0
        )
        handle_error(res)

        return unwrap(key_handle_pointer)

    finally:
        if alg_handle:
            close_alg_handle(alg_handle)