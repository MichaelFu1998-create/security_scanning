def fromts(ts, tzin=None, tzout=None):
    """
    Return the datetime representation of the provided Unix timestamp. By defaults the timestamp is
    interpreted as UTC. If tzin is set it will be interpreted as this timestamp instead. By default
    the output datetime will have UTC time. If tzout is set it will be converted in this timezone
    instead.
    """
    if ts is None:
        return None
    when = datetime.utcfromtimestamp(ts).replace(tzinfo=tzin or utc)
    return totz(when, tzout)