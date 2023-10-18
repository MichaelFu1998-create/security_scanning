def rsa_pkcs1v15_decrypt(private_key, ciphertext):
    """
    Decrypts a byte string using an RSA private key. Uses PKCS#1 v1.5 padding.

    :param private_key:
        A PrivateKey object

    :param ciphertext:
        A byte string of the encrypted data

    :raises:
        ValueError - when any of the parameters contain an invalid value
        TypeError - when any of the parameters are of the wrong type
        OSError - when an error is returned by the OS crypto library

    :return:
        A byte string of the original plaintext
    """

    if not isinstance(private_key, PrivateKey):
        raise TypeError(pretty_message(
            '''
            private_key must an instance of the PrivateKey class, not %s
            ''',
            type_name(private_key)
        ))

    if not isinstance(ciphertext, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(ciphertext)
        ))

    key_length = private_key.byte_size
    buffer = buffer_from_bytes(key_length)
    output_length = new(Security, 'size_t *', key_length)

    if osx_version_info < (10, 8):
        padding = SecurityConst.kSecPaddingNone
    else:
        padding = SecurityConst.kSecPaddingPKCS1

    result = Security.SecKeyDecrypt(
        private_key.sec_key_ref,
        padding,
        ciphertext,
        len(ciphertext),
        buffer,
        output_length
    )
    handle_sec_error(result)

    output = bytes_from_buffer(buffer, deref(output_length))

    if osx_version_info < (10, 8):
        output = remove_pkcs1v15_encryption_padding(key_length, output)

    return output