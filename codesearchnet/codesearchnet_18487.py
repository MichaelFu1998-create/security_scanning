def to_bytes(data: Union[str, bytes]) -> bytes:
    """
    :param data: Data to convert to bytes.
    :type data: Union[str, bytes]
    :return: `data` encoded to UTF8.
    :rtype: bytes
    """
    if isinstance(data, bytes):
        return data
    return data.encode('utf-8')