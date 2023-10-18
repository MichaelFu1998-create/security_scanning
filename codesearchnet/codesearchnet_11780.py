def pretty_bytes(bytes): # pylint: disable=redefined-builtin
    """
    Scales a byte count to the largest scale with a small whole number
    that's easier to read.
    Returns a tuple of the format (scaled_float, unit_string).
    """
    if not bytes:
        return bytes, 'bytes'
    sign = bytes/float(bytes)
    bytes = abs(bytes)
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            #return "%3.1f %s" % (bytes, x)
            return sign*bytes, x
        bytes /= 1024.0