def _bcrypt_encrypt(certificate_or_public_key, data, rsa_oaep_padding=False):
    """
    Encrypts a value using an RSA public key via CNG

    :param certificate_or_public_key:
        A Certificate or PublicKey instance to encrypt with

    :param data:
        A byte string of the data to encrypt

    :param rsa_oaep_padding:
        If OAEP padding should be used instead of PKCS#1 v1.5

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the ciphertext
    """

    flags = BcryptConst.BCRYPT_PAD_PKCS1
    if rsa_oaep_padding is True:
        flags = BcryptConst.BCRYPT_PAD_OAEP

        padding_info_struct_pointer = struct(bcrypt, 'BCRYPT_OAEP_PADDING_INFO')
        padding_info_struct = unwrap(padding_info_struct_pointer)
        # This has to be assigned to a variable to prevent cffi from gc'ing it
        hash_buffer = buffer_from_unicode(BcryptConst.BCRYPT_SHA1_ALGORITHM)
        padding_info_struct.pszAlgId = cast(bcrypt, 'wchar_t *', hash_buffer)
        padding_info_struct.pbLabel = null()
        padding_info_struct.cbLabel = 0
        padding_info = cast(bcrypt, 'void *', padding_info_struct_pointer)
    else:
        padding_info = null()

    out_len = new(bcrypt, 'ULONG *')
    res = bcrypt.BCryptEncrypt(
        certificate_or_public_key.key_handle,
        data,
        len(data),
        padding_info,
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

    res = bcrypt.BCryptEncrypt(
        certificate_or_public_key.key_handle,
        data,
        len(data),
        padding_info,
        null(),
        0,
        buffer,
        buffer_len,
        out_len,
        flags
    )
    handle_error(res)

    return bytes_from_buffer(buffer, deref(out_len))