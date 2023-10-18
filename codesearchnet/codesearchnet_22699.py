def ts(when, tz=None):
    """
    Return a Unix timestamp in seconds for the provided datetime. The `totz` function is called
    on the datetime to convert it to the provided timezone. It will be converted to UTC if no
    timezone is provided.
    """
    if not when:
        return None
    when = totz(when, tz)
    return calendar.timegm(when.timetuple())