def _decrypt_encrypted_data(encryption_algorithm_info, encrypted_content, password):
    """
    Decrypts encrypted ASN.1 data

    :param encryption_algorithm_info:
        An instance of asn1crypto.pkcs5.Pkcs5EncryptionAlgorithm

    :param encrypted_content:
        A byte string of the encrypted content

    :param password:
        A byte string of the encrypted content's password

    :return:
        A byte string of the decrypted plaintext
    """

    decrypt_func = crypto_funcs[encryption_algorithm_info.encryption_cipher]

    # Modern, PKCS#5 PBES2-based encryption
    if encryption_algorithm_info.kdf == 'pbkdf2':

        if encryption_algorithm_info.encryption_cipher == 'rc5':
            raise ValueError(pretty_message(
                '''
                PBES2 encryption scheme utilizing RC5 encryption is not supported
                '''
            ))

        enc_key = pbkdf2(
            encryption_algorithm_info.kdf_hmac,
            password,
            encryption_algorithm_info.kdf_salt,
            encryption_algorithm_info.kdf_iterations,
            encryption_algorithm_info.key_length
        )
        enc_iv = encryption_algorithm_info.encryption_iv

        plaintext = decrypt_func(enc_key, encrypted_content, enc_iv)

    elif encryption_algorithm_info.kdf == 'pbkdf1':
        derived_output = pbkdf1(
            encryption_algorithm_info.kdf_hmac,
            password,
            encryption_algorithm_info.kdf_salt,
            encryption_algorithm_info.kdf_iterations,
            encryption_algorithm_info.key_length + 8
        )
        enc_key = derived_output[0:8]
        enc_iv = derived_output[8:16]

        plaintext = decrypt_func(enc_key, encrypted_content, enc_iv)

    elif encryption_algorithm_info.kdf == 'pkcs12_kdf':
        enc_key = pkcs12_kdf(
            encryption_algorithm_info.kdf_hmac,
            password,
            encryption_algorithm_info.kdf_salt,
            encryption_algorithm_info.kdf_iterations,
            encryption_algorithm_info.key_length,
            1  # ID 1 is for generating a key
        )

        # Since RC4 is a stream cipher, we don't use an IV
        if encryption_algorithm_info.encryption_cipher == 'rc4':
            plaintext = decrypt_func(enc_key, encrypted_content)

        else:
            enc_iv = pkcs12_kdf(
                encryption_algorithm_info.kdf_hmac,
                password,
                encryption_algorithm_info.kdf_salt,
                encryption_algorithm_info.kdf_iterations,
                encryption_algorithm_info.encryption_block_size,
                2   # ID 2 is for generating an IV
            )
            plaintext = decrypt_func(enc_key, encrypted_content, enc_iv)

    return plaintext