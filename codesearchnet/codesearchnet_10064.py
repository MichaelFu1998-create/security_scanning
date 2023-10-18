def _cert_details(cert_pointer):
    """
    Return the certificate and a hash of it

    :param cert_pointer:
        A SecCertificateRef

    :return:
        A 2-element tuple:
         - [0]: A byte string of the SHA1 hash of the cert
         - [1]: A byte string of the DER-encoded contents of the cert
    """

    data_pointer = None

    try:
        data_pointer = Security.SecCertificateCopyData(cert_pointer)
        der_cert = CFHelpers.cf_data_to_bytes(data_pointer)
        cert_hash = hashlib.sha1(der_cert).digest()

        return (der_cert, cert_hash)

    finally:
        if data_pointer is not None:
            CoreFoundation.CFRelease(data_pointer)