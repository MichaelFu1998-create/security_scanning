def _parse_key(stream):
    """Parse key, value combination
    returns :
        Parsed key (string)
    """
    logger.debug("parsing key")

    key = stream.advance_past_chars(["="])

    logger.debug("parsed key:")
    logger.debug("%s", fmt_green(key))
    return key