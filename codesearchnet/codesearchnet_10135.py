def _load_x509(certificate):
    """
    Loads an ASN.1 object of an x509 certificate into a Certificate object

    :param certificate:
        An asn1crypto.x509.Certificate object

    :return:
        A Certificate object
    """

    source = certificate.dump()

    cf_source = None
    try:
        cf_source = CFHelpers.cf_data_from_bytes(source)
        sec_key_ref = Security.SecCertificateCreateWithData(CoreFoundation.kCFAllocatorDefault, cf_source)
        return Certificate(sec_key_ref, certificate)

    finally:
        if cf_source:
            CoreFoundation.CFRelease(cf_source)