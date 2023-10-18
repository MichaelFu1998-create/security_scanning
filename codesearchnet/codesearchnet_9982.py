def _bcrypt_generate_pair(algorithm, bit_size=None, curve=None):
    """
    Generates a public/private key pair using CNG

    :param algorithm:
        The key algorithm - "rsa", "dsa" or "ec"

    :param bit_size:
        An integer - used for "rsa" and "dsa". For "rsa" the value maye be 1024,
        2048, 3072 or 4096. For "dsa" the value may be 1024, plus 2048 or 3072
        if on Windows 8 or newer.

    :param curve:
        A unicode string - used for "ec" keys. Valid values include "secp256r1",
        "secp384r1" and "secp521r1".

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A 2-element tuple of (PublicKey, PrivateKey). The contents of each key
        may be saved by calling .asn1.dump().
    """

    if algorithm == 'rsa':
        alg_constant = BcryptConst.BCRYPT_RSA_ALGORITHM
        struct_type = 'BCRYPT_RSAKEY_BLOB'
        private_blob_type = BcryptConst.BCRYPT_RSAFULLPRIVATE_BLOB
        public_blob_type = BcryptConst.BCRYPT_RSAPUBLIC_BLOB

    elif algorithm == 'dsa':
        alg_constant = BcryptConst.BCRYPT_DSA_ALGORITHM
        if bit_size > 1024:
            struct_type = 'BCRYPT_DSA_KEY_BLOB_V2'
        else:
            struct_type = 'BCRYPT_DSA_KEY_BLOB'
        private_blob_type = BcryptConst.BCRYPT_DSA_PRIVATE_BLOB
        public_blob_type = BcryptConst.BCRYPT_DSA_PUBLIC_BLOB

    else:
        alg_constant = {
            'secp256r1': BcryptConst.BCRYPT_ECDSA_P256_ALGORITHM,
            'secp384r1': BcryptConst.BCRYPT_ECDSA_P384_ALGORITHM,
            'secp521r1': BcryptConst.BCRYPT_ECDSA_P521_ALGORITHM,
        }[curve]
        bit_size = {
            'secp256r1': 256,
            'secp384r1': 384,
            'secp521r1': 521,
        }[curve]
        struct_type = 'BCRYPT_ECCKEY_BLOB'
        private_blob_type = BcryptConst.BCRYPT_ECCPRIVATE_BLOB
        public_blob_type = BcryptConst.BCRYPT_ECCPUBLIC_BLOB

    alg_handle = open_alg_handle(alg_constant)
    key_handle_pointer = new(bcrypt, 'BCRYPT_KEY_HANDLE *')
    res = bcrypt.BCryptGenerateKeyPair(alg_handle, key_handle_pointer, bit_size, 0)
    handle_error(res)
    key_handle = unwrap(key_handle_pointer)

    res = bcrypt.BCryptFinalizeKeyPair(key_handle, 0)
    handle_error(res)

    private_out_len = new(bcrypt, 'ULONG *')
    res = bcrypt.BCryptExportKey(key_handle, null(), private_blob_type, null(), 0, private_out_len, 0)
    handle_error(res)

    private_buffer_length = deref(private_out_len)
    private_buffer = buffer_from_bytes(private_buffer_length)
    res = bcrypt.BCryptExportKey(
        key_handle,
        null(),
        private_blob_type,
        private_buffer,
        private_buffer_length,
        private_out_len,
        0
    )
    handle_error(res)
    private_blob_struct_pointer = struct_from_buffer(bcrypt, struct_type, private_buffer)
    private_blob_struct = unwrap(private_blob_struct_pointer)
    struct_size = sizeof(bcrypt, private_blob_struct)
    private_blob = bytes_from_buffer(private_buffer, private_buffer_length)[struct_size:]

    if algorithm == 'rsa':
        private_key = _bcrypt_interpret_rsa_key_blob('private', private_blob_struct, private_blob)
    elif algorithm == 'dsa':
        if bit_size > 1024:
            private_key = _bcrypt_interpret_dsa_key_blob('private', 2, private_blob_struct, private_blob)
        else:
            private_key = _bcrypt_interpret_dsa_key_blob('private', 1, private_blob_struct, private_blob)
    else:
        private_key = _bcrypt_interpret_ec_key_blob('private', private_blob_struct, private_blob)

    public_out_len = new(bcrypt, 'ULONG *')
    res = bcrypt.BCryptExportKey(key_handle, null(), public_blob_type, null(), 0, public_out_len, 0)
    handle_error(res)

    public_buffer_length = deref(public_out_len)
    public_buffer = buffer_from_bytes(public_buffer_length)
    res = bcrypt.BCryptExportKey(
        key_handle,
        null(),
        public_blob_type,
        public_buffer,
        public_buffer_length,
        public_out_len,
        0
    )
    handle_error(res)
    public_blob_struct_pointer = struct_from_buffer(bcrypt, struct_type, public_buffer)
    public_blob_struct = unwrap(public_blob_struct_pointer)
    struct_size = sizeof(bcrypt, public_blob_struct)
    public_blob = bytes_from_buffer(public_buffer, public_buffer_length)[struct_size:]

    if algorithm == 'rsa':
        public_key = _bcrypt_interpret_rsa_key_blob('public', public_blob_struct, public_blob)
    elif algorithm == 'dsa':
        if bit_size > 1024:
            public_key = _bcrypt_interpret_dsa_key_blob('public', 2, public_blob_struct, public_blob)
        else:
            public_key = _bcrypt_interpret_dsa_key_blob('public', 1, public_blob_struct, public_blob)
    else:
        public_key = _bcrypt_interpret_ec_key_blob('public', public_blob_struct, public_blob)

    return (load_public_key(public_key), load_private_key(private_key))