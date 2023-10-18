def parse_certificate(data):
    """
    Loads a certificate from a DER or PEM-formatted file. Supports X.509
    certificates only.

    :param data:
        A byte string to load the certificate from

    :raises:
        ValueError - when the data does not appear to contain a certificate

    :return:
        An asn1crypto.x509.Certificate object
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
        key_type, _, data = _unarmor_pem(data)

        if key_type == 'private key':
            raise ValueError(pretty_message(
                '''
                The data specified does not appear to be a certificate, but
                rather a private key
                '''
            ))

        if key_type == 'public key':
            raise ValueError(pretty_message(
                '''
                The data specified does not appear to be a certificate, but
                rather a public key
                '''
            ))

    if key_type is None or key_type == 'certificate':
        try:
            return x509.Certificate.load(data)
        except (ValueError):
            pass  # Data was not a Certificate

    raise ValueError(pretty_message(
        '''
        The data specified does not appear to be a known certificate format
        '''
    ))