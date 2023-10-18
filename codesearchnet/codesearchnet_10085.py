def dump_private_key(private_key, passphrase, encoding='pem', target_ms=200):
    """
    Serializes a private key object into a byte string of the PKCS#8 format

    :param private_key:
        An oscrypto.asymmetric.PrivateKey or asn1crypto.keys.PrivateKeyInfo
        object

    :param passphrase:
        A unicode string of the passphrase to encrypt the private key with.
        A passphrase of None will result in no encryption. A blank string will
        result in a ValueError to help ensure that the lack of passphrase is
        intentional.

    :param encoding:
        A unicode string of "pem" or "der"

    :param target_ms:
        Use PBKDF2 with the number of iterations that takes about this many
        milliseconds on the current machine.

    :raises:
        ValueError - when a blank string is provided for the passphrase

    :return:
        A byte string of the encoded and encrypted public key
    """

    if encoding not in set(['pem', 'der']):
        raise ValueError(pretty_message(
            '''
            encoding must be one of "pem", "der", not %s
            ''',
            repr(encoding)
        ))

    if passphrase is not None:
        if not isinstance(passphrase, str_cls):
            raise TypeError(pretty_message(
                '''
                passphrase must be a unicode string, not %s
                ''',
                type_name(passphrase)
            ))
        if passphrase == '':
            raise ValueError(pretty_message(
                '''
                passphrase may not be a blank string - pass None to disable
                encryption
                '''
            ))

    is_oscrypto = isinstance(private_key, PrivateKey)
    if not isinstance(private_key, keys.PrivateKeyInfo) and not is_oscrypto:
        raise TypeError(pretty_message(
            '''
            private_key must be an instance of oscrypto.asymmetric.PrivateKey
            or asn1crypto.keys.PrivateKeyInfo, not %s
            ''',
            type_name(private_key)
        ))

    if is_oscrypto:
        private_key = private_key.asn1

    output = private_key.dump()

    if passphrase is not None:
        cipher = 'aes256_cbc'
        key_length = 32
        kdf_hmac = 'sha256'
        kdf_salt = rand_bytes(key_length)
        iterations = pbkdf2_iteration_calculator(kdf_hmac, key_length, target_ms=target_ms, quiet=True)
        # Need a bare minimum of 10,000 iterations for PBKDF2 as of 2015
        if iterations < 10000:
            iterations = 10000

        passphrase_bytes = passphrase.encode('utf-8')
        key = pbkdf2(kdf_hmac, passphrase_bytes, kdf_salt, iterations, key_length)
        iv, ciphertext = aes_cbc_pkcs7_encrypt(key, output, None)

        output = keys.EncryptedPrivateKeyInfo({
            'encryption_algorithm': {
                'algorithm': 'pbes2',
                'parameters': {
                    'key_derivation_func': {
                        'algorithm': 'pbkdf2',
                        'parameters': {
                            'salt': algos.Pbkdf2Salt(
                                name='specified',
                                value=kdf_salt
                            ),
                            'iteration_count': iterations,
                            'prf': {
                                'algorithm': kdf_hmac,
                                'parameters': core.Null()
                            }
                        }
                    },
                    'encryption_scheme': {
                        'algorithm': cipher,
                        'parameters': iv
                    }
                }
            },
            'encrypted_data': ciphertext
        }).dump()

    if encoding == 'pem':
        if passphrase is None:
            object_type = 'PRIVATE KEY'
        else:
            object_type = 'ENCRYPTED PRIVATE KEY'
        output = pem.armor(object_type, output)

    return output