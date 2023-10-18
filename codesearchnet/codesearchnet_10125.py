def get_path(temp_dir=None, cache_length=24, cert_callback=None):
    """
    Get the filesystem path to a file that contains OpenSSL-compatible CA certs.

    On OS X and Windows, there are extracted from the system certificate store
    and cached in a file on the filesystem. This path should not be writable
    by other users, otherwise they could inject CA certs into the trust list.

    :param temp_dir:
        The temporary directory to cache the CA certs in on OS X and Windows.
        Needs to have secure permissions so other users can not modify the
        contents.

    :param cache_length:
        The number of hours to cache the CA certs on OS X and Windows

    :param cert_callback:
        A callback that is called once for each certificate in the trust store.
        It should accept two parameters: an asn1crypto.x509.Certificate object,
        and a reason. The reason will be None if the certificate is being
        exported, otherwise it will be a unicode string of the reason it won't.
        This is only called on Windows and OS X when passed to this function.

    :raises:
        oscrypto.errors.CACertsError - when an error occurs exporting/locating certs

    :return:
        The full filesystem path to a CA certs file
    """

    ca_path, temp = _ca_path(temp_dir)

    # Windows and OS X
    if temp and _cached_path_needs_update(ca_path, cache_length):
        empty_set = set()

        any_purpose = '2.5.29.37.0'
        apple_ssl = '1.2.840.113635.100.1.3'
        win_server_auth = '1.3.6.1.5.5.7.3.1'

        with path_lock:
            if _cached_path_needs_update(ca_path, cache_length):
                with open(ca_path, 'wb') as f:
                    for cert, trust_oids, reject_oids in extract_from_system(cert_callback, True):
                        if sys.platform == 'darwin':
                            if trust_oids != empty_set and any_purpose not in trust_oids \
                                    and apple_ssl not in trust_oids:
                                if cert_callback:
                                    cert_callback(Certificate.load(cert), 'implicitly distrusted for TLS')
                                continue
                            if reject_oids != empty_set and (apple_ssl in reject_oids
                                                             or any_purpose in reject_oids):
                                if cert_callback:
                                    cert_callback(Certificate.load(cert), 'explicitly distrusted for TLS')
                                continue
                        elif sys.platform == 'win32':
                            if trust_oids != empty_set and any_purpose not in trust_oids \
                                    and win_server_auth not in trust_oids:
                                if cert_callback:
                                    cert_callback(Certificate.load(cert), 'implicitly distrusted for TLS')
                                continue
                            if reject_oids != empty_set and (win_server_auth in reject_oids
                                                             or any_purpose in reject_oids):
                                if cert_callback:
                                    cert_callback(Certificate.load(cert), 'explicitly distrusted for TLS')
                                continue
                        if cert_callback:
                            cert_callback(Certificate.load(cert), None)
                        f.write(armor('CERTIFICATE', cert))

    if not ca_path:
        raise CACertsError('No CA certs found')

    return ca_path