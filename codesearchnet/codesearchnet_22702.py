def fromtsms(ts, tzin=None, tzout=None):
    """
    Return the Unix timestamp in milliseconds as a datetime object. If tz is set it will be
    converted to the requested timezone otherwise it defaults to UTC.
    """
    if ts is None:
        return None
    when = datetime.utcfromtimestamp(ts / 1000).replace(microsecond=ts % 1000 * 1000)
    when = when.replace(tzinfo=tzin or utc)
    return totz(when, tzout)