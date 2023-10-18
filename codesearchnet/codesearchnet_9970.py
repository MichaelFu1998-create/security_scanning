def _load_x509(certificate):
    """
    Loads an ASN.1 object of an x509 certificate into a Certificate object

    :param certificate:
        An asn1crypto.x509.Certificate object

    :return:
        A Certificate object
    """

    source = certificate.dump()

    buffer = buffer_from_bytes(source)
    evp_pkey = libcrypto.d2i_X509(null(), buffer_pointer(buffer), len(source))
    if is_null(evp_pkey):
        handle_openssl_error(0)
    return Certificate(evp_pkey, certificate)