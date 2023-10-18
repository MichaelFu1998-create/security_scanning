def get_prefix(multicodec):
    """
    Returns prefix for a given multicodec

    :param str multicodec: multicodec codec name
    :return: the prefix for the given multicodec
    :rtype: byte
    :raises ValueError: if an invalid multicodec name is provided
    """
    try:
        prefix = varint.encode(NAME_TABLE[multicodec])
    except KeyError:
        raise ValueError('{} multicodec is not supported.'.format(multicodec))
    return prefix