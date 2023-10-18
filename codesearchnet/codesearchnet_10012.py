def _advapi32_decrypt(private_key, ciphertext, rsa_oaep_padding=False):
    """
    Encrypts a value using an RSA private key via CryptoAPI

    :param private_key:
        A PrivateKey instance to decrypt with

    :param ciphertext:
        A byte string of the data to decrypt

    :param rsa_oaep_padding:
        If OAEP padding should be used instead of PKCS#1 v1.5

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the plaintext
    """

    flags = 0
    if rsa_oaep_padding:
        flags = Advapi32Const.CRYPT_OAEP

    ciphertext = ciphertext[::-1]

    buffer = buffer_from_bytes(ciphertext)
    out_len = new(advapi32, 'DWORD *', len(ciphertext))
    res = advapi32.CryptDecrypt(
        private_key.ex_key_handle,
        null(),
        True,
        flags,
        buffer,
        out_len
    )
    handle_error(res)

    return bytes_from_buffer(buffer, deref(out_len))