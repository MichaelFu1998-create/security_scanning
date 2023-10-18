def _decode_asn1_string(data):
    """Convert ASN.1 string to a Unicode string.
    """
    if isinstance(data, BMPString):
        return bytes(data).decode("utf-16-be")
    else:
        return bytes(data).decode("utf-8")