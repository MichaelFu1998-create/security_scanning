def remove_prefix(bytes_):
    """
    Removes prefix from a prefixed data

    :param bytes bytes_: multicodec prefixed data bytes
    :return: prefix removed data bytes
    :rtype: bytes
    """
    prefix_int = extract_prefix(bytes_)
    prefix = varint.encode(prefix_int)
    return bytes_[len(prefix):]