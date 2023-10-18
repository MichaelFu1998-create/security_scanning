def _parse_array(stream):
    """Parse an array, stream should be passed the initial [
    returns:
        Parsed array
    """

    logger.debug("parsing array")
    arr = []
    while True:
        c = stream.read(1)

        if c in _GDB_MI_VALUE_START_CHARS:
            stream.seek(-1)
            val = _parse_val(stream)
            arr.append(val)
        elif c in _WHITESPACE:
            pass
        elif c == ",":
            pass
        elif c == "]":
            # Stop when this array has finished. Note
            # that elements of this array can be also be arrays.
            break

    logger.debug("parsed array:")
    logger.debug("%s", fmt_green(arr))
    return arr