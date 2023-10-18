def get_codec(bytes_):
    """
    Gets the codec used for prefix the multicodec prefixed data

    :param bytes bytes_: multicodec prefixed data bytes
    :return: name of the multicodec used to prefix
    :rtype: str
    """
    prefix = extract_prefix(bytes_)
    try:
        return CODE_TABLE[prefix]
    except KeyError:
        raise ValueError('Prefix {} not present in the lookup table'.format(prefix))