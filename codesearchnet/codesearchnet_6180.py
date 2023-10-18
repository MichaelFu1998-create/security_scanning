def to_unicode_safe(s):
    """Convert a binary string to Unicode using UTF-8 (fallback to ISO-8859-1)."""
    try:
        u = compat.to_unicode(s, "utf8")
    except ValueError:
        _logger.error(
            "to_unicode_safe({!r}) *** UTF-8 failed. Trying ISO-8859-1".format(s)
        )
        u = compat.to_unicode(s, "ISO-8859-1")
    return u