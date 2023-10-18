def from_bytes(data: Union[str, bytes]) -> str:
    """
    :param data: A UTF8 byte string.
    :type data: Union[str, bytes]
    :return: `data` decoded from UTF8.
    :rtype: str
    """
    if isinstance(data, str):
        return data
    return str(data, 'utf-8')