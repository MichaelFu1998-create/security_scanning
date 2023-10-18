def buffer_format(frmt: str) -> BufferFormat:
    """
    Look up info about a buffer format
    :param frmt: format string such as 'f', 'i' and 'u'
    :return: BufferFormat instance
    """
    try:
        return BUFFER_FORMATS[frmt]
    except KeyError:
        raise ValueError("Buffer format '{}' unknown. Valid formats: {}".format(
            frmt, BUFFER_FORMATS.keys()
        ))