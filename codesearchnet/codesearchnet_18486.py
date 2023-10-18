def b64_decode(data: bytes) -> bytes:
    """
    :param data: Base 64 encoded data to decode.
    :type data: bytes
    :return: Base 64 decoded data.
    :rtype: bytes
    """
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'=' * (4 - missing_padding)
    return urlsafe_b64decode(data)