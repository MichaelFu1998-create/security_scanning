def dump_certificate(certificate, encoding='pem'):
    """
    Serializes a certificate object into a byte string

    :param certificate:
        An oscrypto.asymmetric.Certificate or asn1crypto.x509.Certificate object

    :param encoding:
        A unicode string of "pem" or "der"

    :return:
        A byte string of the encoded certificate
    """

    if encoding not in set(['pem', 'der']):
        raise ValueError(pretty_message(
            '''
            encoding must be one of "pem", "der", not %s
            ''',
            repr(encoding)
        ))

    is_oscrypto = isinstance(certificate, Certificate)
    if not isinstance(certificate, x509.Certificate) and not is_oscrypto:
        raise TypeError(pretty_message(
            '''
            certificate must be an instance of oscrypto.asymmetric.Certificate
            or asn1crypto.x509.Certificate, not %s
            ''',
            type_name(certificate)
        ))

    if is_oscrypto:
        certificate = certificate.asn1

    output = certificate.dump()
    if encoding == 'pem':
        output = pem.armor('CERTIFICATE', output)
    return output