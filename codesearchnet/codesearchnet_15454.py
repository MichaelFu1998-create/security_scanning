def add_prefix(multicodec, bytes_):
    """
    Adds multicodec prefix to the given bytes input

    :param str multicodec: multicodec to use for prefixing
    :param bytes bytes_: data to prefix
    :return: prefixed byte data
    :rtype: bytes
    """
    prefix = get_prefix(multicodec)
    return b''.join([prefix, bytes_])