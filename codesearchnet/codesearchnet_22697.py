def totz(when, tz=None):
    """
    Return a date, time, or datetime converted to a datetime in the given timezone. If when is a
    datetime and has no timezone it is assumed to be local time. Date and time objects are also
    assumed to be UTC. The tz value defaults to UTC. Raise TypeError if when cannot be converted to
    a datetime.
    """
    if when is None:
        return None
    when = to_datetime(when)
    if when.tzinfo is None:
        when = when.replace(tzinfo=localtz)
    return when.astimezone(tz or utc)