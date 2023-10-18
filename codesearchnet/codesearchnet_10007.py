def _bcrypt_sign(private_key, data, hash_algorithm, rsa_pss_padding=False):
    """
    Generates an RSA, DSA or ECDSA signature via CNG

    :param private_key:
        The PrivateKey to generate the signature with

    :param data:
        A byte string of the data the signature is for

    :param hash_algorithm:
        A unicode string of "md5", "sha1", "sha256", "sha384", "sha512" or "raw"

    :param rsa_pss_padding:
        If PSS padding should be used for RSA keys

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the signature
    """

    if hash_algorithm == 'raw':
        digest = data
    else:
        hash_constant = {
            'md5': BcryptConst.BCRYPT_MD5_ALGORITHM,
            'sha1': BcryptConst.BCRYPT_SHA1_ALGORITHM,
            'sha256': BcryptConst.BCRYPT_SHA256_ALGORITHM,
            'sha384': BcryptConst.BCRYPT_SHA384_ALGORITHM,
            'sha512': BcryptConst.BCRYPT_SHA512_ALGORITHM
        }[hash_algorithm]

        digest = getattr(hashlib, hash_algorithm)(data).digest()

    padding_info = null()
    flags = 0

    if private_key.algorithm == 'rsa':
        if rsa_pss_padding:
            hash_length = {
                'md5': 16,
                'sha1': 20,
                'sha256': 32,
                'sha384': 48,
                'sha512': 64
            }[hash_algorithm]

            flags = BcryptConst.BCRYPT_PAD_PSS
            padding_info_struct_pointer = struct(bcrypt, 'BCRYPT_PSS_PADDING_INFO')
            padding_info_struct = unwrap(padding_info_struct_pointer)
            # This has to be assigned to a variable to prevent cffi from gc'ing it
            hash_buffer = buffer_from_unicode(hash_constant)
            padding_info_struct.pszAlgId = cast(bcrypt, 'wchar_t *', hash_buffer)
            padding_info_struct.cbSalt = hash_length
        else:
            flags = BcryptConst.BCRYPT_PAD_PKCS1
            padding_info_struct_pointer = struct(bcrypt, 'BCRYPT_PKCS1_PADDING_INFO')
            padding_info_struct = unwrap(padding_info_struct_pointer)
            # This has to be assigned to a variable to prevent cffi from gc'ing it
            if hash_algorithm == 'raw':
                padding_info_struct.pszAlgId = null()
            else:
                hash_buffer = buffer_from_unicode(hash_constant)
                padding_info_struct.pszAlgId = cast(bcrypt, 'wchar_t *', hash_buffer)
        padding_info = cast(bcrypt, 'void *', padding_info_struct_pointer)

    if private_key.algorithm == 'dsa' and private_key.bit_size > 1024 and hash_algorithm in set(['md5', 'sha1']):
        raise ValueError(pretty_message(
            '''
            Windows does not support sha1 signatures with DSA keys based on
            sha224, sha256 or sha512
            '''
        ))

    out_len = new(bcrypt, 'DWORD *')
    res = bcrypt.BCryptSignHash(
        private_key.key_handle,
        padding_info,
        digest,
        len(digest),
        null(),
        0,
        out_len,
        flags
    )
    handle_error(res)

    buffer_len = deref(out_len)
    buffer = buffer_from_bytes(buffer_len)

    if private_key.algorithm == 'rsa':
        padding_info = cast(bcrypt, 'void *', padding_info_struct_pointer)

    res = bcrypt.BCryptSignHash(
        private_key.key_handle,
        padding_info,
        digest,
        len(digest),
        buffer,
        buffer_len,
        out_len,
        flags
    )
    handle_error(res)
    signature = bytes_from_buffer(buffer, deref(out_len))

    if private_key.algorithm != 'rsa':
        # Windows doesn't use the ASN.1 Sequence for DSA/ECDSA signatures,
        # so we have to convert it here for the verification to work
        signature = algos.DSASignature.from_p1363(signature).dump()

    return signature