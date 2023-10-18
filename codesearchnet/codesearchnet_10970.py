def attribute_format(frmt: str) -> BufferFormat:
    """
    Look up info about an attribute format
    :param frmt: Format of an
    :return: BufferFormat instance
    """
    try:
        return ATTRIBUTE_FORMATS[frmt]
    except KeyError:
        raise ValueError("Buffer format '{}' unknown. Valid formats: {}".format(
            frmt, ATTRIBUTE_FORMATS.keys()
        ))