def _parse_key_val(stream):
    """Parse key, value combination
    return (tuple):
        Parsed key (string)
        Parsed value (either a string, array, or dict)
    """

    logger.debug("parsing key/val")
    key = _parse_key(stream)
    val = _parse_val(stream)

    logger.debug("parsed key/val")
    logger.debug("%s", fmt_green(key))
    logger.debug("%s", fmt_green(val))

    return key, val