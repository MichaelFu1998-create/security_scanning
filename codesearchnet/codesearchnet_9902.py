def _parse_val(stream):
    """Parse value from string
    returns:
        Parsed value (either a string, array, or dict)
    """

    logger.debug("parsing value")

    while True:
        c = stream.read(1)

        if c == "{":
            # Start object
            val = _parse_dict(stream)
            break

        elif c == "[":
            # Start of an array
            val = _parse_array(stream)
            break

        elif c == '"':
            # Start of a string
            val = stream.advance_past_string_with_gdb_escapes()
            break

        elif _DEBUG:
            raise ValueError("unexpected character: %s" % c)

        else:
            print(
                'pygdbmi warning: encountered unexpected character: "%s". Continuing.'
                % c
            )
            val = ""  # this will be overwritten if there are more characters to be read

    logger.debug("parsed value:")
    logger.debug("%s", fmt_green(val))

    return val