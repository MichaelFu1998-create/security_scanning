def parse_private(data, password=None):
    """
    Loads a private key from a DER or PEM-formatted file. Supports RSA, DSA and
    EC private keys. Works with the follow formats:

     - RSAPrivateKey (PKCS#1)
     - ECPrivateKey (SECG SEC1 V2)
     - DSAPrivateKey (OpenSSL)
     - PrivateKeyInfo (RSA/DSA/EC - PKCS#8)
     - EncryptedPrivateKeyInfo (RSA/DSA/EC - PKCS#8)
     - Encrypted RSAPrivateKey (PEM only, OpenSSL)
     - Encrypted DSAPrivateKey (PEM only, OpenSSL)
     - Encrypted ECPrivateKey (PEM only, OpenSSL)

    :param data:
        A byte string to load the private key from

    :param password:
        The password to unencrypt the private key

    :raises:
        ValueError - when the data does not appear to contain a private key, or the password is invalid

    :return:
        An asn1crypto.keys.PrivateKeyInfo object
    """

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    if password is not None:
        if not isinstance(password, byte_cls):
            raise TypeError(pretty_message(
                '''
                password must be a byte string, not %s
                ''',
                type_name(password)
            ))
    else:
        password = b''

    # Appears to be PEM formatted
    if data[0:5] == b'-----':
        key_type, _, data = _unarmor_pem(data, password)

        if key_type == 'public key':
            raise ValueError(pretty_message(
                '''
                The data specified does not appear to be a private key, but
                rather a public key
                '''
            ))

        if key_type == 'certificate':
            raise ValueError(pretty_message(
                '''
                The data specified does not appear to be a private key, but
                rather a certificate
                '''
            ))

    try:
        pki = keys.PrivateKeyInfo.load(data)
        # Call .native to fully parse since asn1crypto is lazy
        pki.native
        return pki
    except (ValueError):
        pass  # Data was not PrivateKeyInfo

    try:
        parsed_wrapper = keys.EncryptedPrivateKeyInfo.load(data)
        encryption_algorithm_info = parsed_wrapper['encryption_algorithm']
        encrypted_data = parsed_wrapper['encrypted_data'].native
        decrypted_data = _decrypt_encrypted_data(encryption_algorithm_info, encrypted_data, password)
        pki = keys.PrivateKeyInfo.load(decrypted_data)
        # Call .native to fully parse since asn1crypto is lazy
        pki.native
        return pki
    except (ValueError):
        pass  # Data was not EncryptedPrivateKeyInfo

    try:
        parsed = keys.RSAPrivateKey.load(data)
        # Call .native to fully parse since asn1crypto is lazy
        parsed.native
        return keys.PrivateKeyInfo.wrap(parsed, 'rsa')
    except (ValueError):
        pass  # Data was not an RSAPrivateKey

    try:
        parsed = keys.DSAPrivateKey.load(data)
        # Call .native to fully parse since asn1crypto is lazy
        parsed.native
        return keys.PrivateKeyInfo.wrap(parsed, 'dsa')
    except (ValueError):
        pass  # Data was not a DSAPrivateKey

    try:
        parsed = keys.ECPrivateKey.load(data)
        # Call .native to fully parse since asn1crypto is lazy
        parsed.native
        return keys.PrivateKeyInfo.wrap(parsed, 'ec')
    except (ValueError):
        pass  # Data was not an ECPrivateKey

    raise ValueError(pretty_message(
        '''
        The data specified does not appear to be a known private key format
        '''
    ))