def system_path():
    """
    Tries to find a CA certs bundle in common locations

    :raises:
        OSError - when no valid CA certs bundle was found on the filesystem

    :return:
        The full filesystem path to a CA certs bundle file
    """

    ca_path = None

    # Common CA cert paths
    paths = [
        '/usr/lib/ssl/certs/ca-certificates.crt',
        '/etc/ssl/certs/ca-certificates.crt',
        '/etc/ssl/certs/ca-bundle.crt',
        '/etc/pki/tls/certs/ca-bundle.crt',
        '/etc/ssl/ca-bundle.pem',
        '/usr/local/share/certs/ca-root-nss.crt',
        '/etc/ssl/cert.pem'
    ]

    # First try SSL_CERT_FILE
    if 'SSL_CERT_FILE' in os.environ:
        paths.insert(0, os.environ['SSL_CERT_FILE'])

    for path in paths:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            ca_path = path
            break

    if not ca_path:
        raise OSError(pretty_message(
            '''
            Unable to find a CA certs bundle in common locations - try
            setting the SSL_CERT_FILE environmental variable
            '''
        ))

    return ca_path