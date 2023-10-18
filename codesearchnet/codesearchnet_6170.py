def _parse_gmt_time(timestring):
    """Return a standard time tuple (see time and calendar), for a date/time string."""
    # Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123
    try:
        return time.strptime(timestring, "%a, %d %b %Y %H:%M:%S GMT")
    except Exception:
        pass

    # Sunday, 06-Nov-94 08:49:37 GMT ; RFC 850, obsoleted by RFC 1036
    try:
        return time.strptime(timestring, "%A %d-%b-%y %H:%M:%S GMT")
    except Exception:
        pass

    # Sun Nov  6 08:49:37 1994       ; ANSI C's asctime() format
    try:
        return time.strptime(timestring, "%a %b %d %H:%M:%S %Y")
    except Exception:
        pass

    # Sun Nov  6 08:49:37 1994 +0100      ; ANSI C's asctime() format with
    # timezon
    try:
        return parsedate(timestring)
    except Exception:
        pass

    return None