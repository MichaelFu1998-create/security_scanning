def b64_encode(data: bytes) -> bytes:
    """
    :param data: Data the encode.
    :type data: bytes
    :return: Base 64 encoded data with padding removed.
    :rtype: bytes
    """
    encoded = urlsafe_b64encode(data)
    return encoded.replace(b'=', b'')