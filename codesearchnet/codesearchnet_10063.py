def _cert_callback(callback, der_cert, reason):
    """
    Constructs an asn1crypto.x509.Certificate object and calls the export
    callback

    :param callback:
        The callback to call

    :param der_cert:
        A byte string of the DER-encoded certificate

    :param reason:
        None if cert is being exported, or a unicode string of the reason it
        is not being exported
    """

    if not callback:
        return
    callback(x509.Certificate.load(der_cert), reason)