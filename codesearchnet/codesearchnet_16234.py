def maybe_decode_header(header):
    """
    Decodes an encoded 7-bit ASCII header value into it's actual value.
    """
    value, encoding = decode_header(header)[0]
    if encoding:
        return value.decode(encoding)
    else:
        return value