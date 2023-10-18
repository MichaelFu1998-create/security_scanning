def tsms(when, tz=None):
    """
    Return a Unix timestamp in milliseconds for the provided datetime. The `totz` function is
    called on the datetime to convert it to the provided timezone. It will be converted to UTC if
    no timezone is provided.
    """
    if not when:
        return None
    when = totz(when, tz)
    return calendar.timegm(when.timetuple()) * 1000 + int(round(when.microsecond / 1000.0))