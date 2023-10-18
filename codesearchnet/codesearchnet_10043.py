def _advapi32_create_handles(cipher, key, iv):
    """
    Creates an HCRYPTPROV and HCRYPTKEY for symmetric encryption/decryption. The
    HCRYPTPROV must be released by close_context_handle() and the
    HCRYPTKEY must be released by advapi32.CryptDestroyKey() when done.

    :param cipher:
        A unicode string of "aes", "des", "tripledes_2key", "tripledes_3key",
        "rc2", "rc4"

    :param key:
        A byte string of the symmetric key

    :param iv:
        The initialization vector - a byte string - unused for RC4

    :return:
        A tuple of (HCRYPTPROV, HCRYPTKEY)
    """

    context_handle = None

    if cipher == 'aes':
        algorithm_id = {
            16: Advapi32Const.CALG_AES_128,
            24: Advapi32Const.CALG_AES_192,
            32: Advapi32Const.CALG_AES_256,
        }[len(key)]
    else:
        algorithm_id = {
            'des': Advapi32Const.CALG_DES,
            'tripledes_2key': Advapi32Const.CALG_3DES_112,
            'tripledes_3key': Advapi32Const.CALG_3DES,
            'rc2': Advapi32Const.CALG_RC2,
            'rc4': Advapi32Const.CALG_RC4,
        }[cipher]

    provider = Advapi32Const.MS_ENH_RSA_AES_PROV
    context_handle = open_context_handle(provider, verify_only=False)

    blob_header_pointer = struct(advapi32, 'BLOBHEADER')
    blob_header = unwrap(blob_header_pointer)
    blob_header.bType = Advapi32Const.PLAINTEXTKEYBLOB
    blob_header.bVersion = Advapi32Const.CUR_BLOB_VERSION
    blob_header.reserved = 0
    blob_header.aiKeyAlg = algorithm_id

    blob_struct_pointer = struct(advapi32, 'PLAINTEXTKEYBLOB')
    blob_struct = unwrap(blob_struct_pointer)
    blob_struct.hdr = blob_header
    blob_struct.dwKeySize = len(key)

    blob = struct_bytes(blob_struct_pointer) + key

    flags = 0
    if cipher in set(['rc2', 'rc4']) and len(key) == 5:
        flags = Advapi32Const.CRYPT_NO_SALT

    key_handle_pointer = new(advapi32, 'HCRYPTKEY *')
    res = advapi32.CryptImportKey(
        context_handle,
        blob,
        len(blob),
        null(),
        flags,
        key_handle_pointer
    )
    handle_error(res)

    key_handle = unwrap(key_handle_pointer)

    if cipher == 'rc2':
        buf = new(advapi32, 'DWORD *', len(key) * 8)
        res = advapi32.CryptSetKeyParam(
            key_handle,
            Advapi32Const.KP_EFFECTIVE_KEYLEN,
            buf,
            0
        )
        handle_error(res)

    if cipher != 'rc4':
        res = advapi32.CryptSetKeyParam(
            key_handle,
            Advapi32Const.KP_IV,
            iv,
            0
        )
        handle_error(res)

        buf = new(advapi32, 'DWORD *', Advapi32Const.CRYPT_MODE_CBC)
        res = advapi32.CryptSetKeyParam(
            key_handle,
            Advapi32Const.KP_MODE,
            buf,
            0
        )
        handle_error(res)

        buf = new(advapi32, 'DWORD *', Advapi32Const.PKCS5_PADDING)
        res = advapi32.CryptSetKeyParam(
            key_handle,
            Advapi32Const.KP_PADDING,
            buf,
            0
        )
        handle_error(res)

    return (context_handle, key_handle)