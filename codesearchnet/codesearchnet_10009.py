def _advapi32_encrypt(certificate_or_public_key, data, rsa_oaep_padding=False):
    """
    Encrypts a value using an RSA public key via CryptoAPI

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

    flags = 0
    if rsa_oaep_padding:
        flags = Advapi32Const.CRYPT_OAEP

    out_len = new(advapi32, 'DWORD *', len(data))
    res = advapi32.CryptEncrypt(
        certificate_or_public_key.ex_key_handle,
        null(),
        True,
        flags,
        null(),
        out_len,
        0
    )
    handle_error(res)

    buffer_len = deref(out_len)
    buffer = buffer_from_bytes(buffer_len)
    write_to_buffer(buffer, data)

    pointer_set(out_len, len(data))
    res = advapi32.CryptEncrypt(
        certificate_or_public_key.ex_key_handle,
        null(),
        True,
        flags,
        buffer,
        out_len,
        buffer_len
    )
    handle_error(res)

    return bytes_from_buffer(buffer, deref(out_len))[::-1]