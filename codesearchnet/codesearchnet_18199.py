def generate_wildcard_pem_bytes():
    """
    Generate a wildcard (subject name '*') self-signed certificate valid for
    10 years.

    https://cryptography.io/en/latest/x509/tutorial/#creating-a-self-signed-certificate

    :return: Bytes representation of the PEM certificate data
    """
    key = generate_private_key(u'rsa')
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, u'*')])
    cert = (
        x509.CertificateBuilder()
        .issuer_name(name)
        .subject_name(name)
        .not_valid_before(datetime.today() - timedelta(days=1))
        .not_valid_after(datetime.now() + timedelta(days=3650))
        .serial_number(int(uuid.uuid4()))
        .public_key(key.public_key())
        .sign(
            private_key=key,
            algorithm=hashes.SHA256(),
            backend=default_backend())
        )

    return b''.join((
        key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()),
        cert.public_bytes(serialization.Encoding.PEM)
    ))