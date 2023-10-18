def parse_public(data):
    """
    Loads a public key from a DER or PEM-formatted file. Supports RSA, DSA and
    EC public keys. For RSA keys, both the old RSAPublicKey and
    SubjectPublicKeyInfo structures are supported. Also allows extracting a
    public key from an X.509 certificate.

    :param data:
        A byte string to load the public key from

    :raises:
        ValueError - when the data does not appear to contain a public key

    :return:
        An asn1crypto.keys.PublicKeyInfo object
    """

    if not isinstance(data, byte_cls):
        raise TypeError(pretty_message(
            '''
            data must be a byte string, not %s
            ''',
            type_name(data)
        ))

    key_type = None

    # Appears to be PEM formatted
    if data[0:5] == b'-----':
        key_type, algo, data = _unarmor_pem(data)

        if key_type == 'private key':
            raise ValueError(pretty_message(
                '''
                The data specified does not appear to be a public key or
                certificate, but rather a private key
                '''
            ))

        # When a public key returning from _unarmor_pem has a known algorithm
        # of RSA, that means the DER structure is of the type RSAPublicKey, so
        # we need to wrap it in the PublicKeyInfo structure.
        if algo == 'rsa':
            return keys.PublicKeyInfo.wrap(data, 'rsa')

    if key_type is None or key_type == 'public key':
        try:
            pki = keys.PublicKeyInfo.load(data)
            # Call .native to fully parse since asn1crypto is lazy
            pki.native
            return pki
        except (ValueError):
            pass  # Data was not PublicKeyInfo

        try:
            rpk = keys.RSAPublicKey.load(data)
            # Call .native to fully parse since asn1crypto is lazy
            rpk.native
            return keys.PublicKeyInfo.wrap(rpk, 'rsa')
        except (ValueError):
            pass  # Data was not an RSAPublicKey

    if key_type is None or key_type == 'certificate':
        try:
            parsed_cert = x509.Certificate.load(data)
            key_info = parsed_cert['tbs_certificate']['subject_public_key_info']
            return key_info
        except (ValueError):
            pass  # Data was not a cert

    raise ValueError('The data specified does not appear to be a known public key or certificate format')