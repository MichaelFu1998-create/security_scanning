def timestamp_with_tzinfo(dt):
    """
    Serialize a date/time value into an ISO8601 text representation
    adjusted (if needed) to UTC timezone.

    For instance:
    >>> serialize_date(datetime(2012, 4, 10, 22, 38, 20, 604391))
    '2012-04-10T22:38:20.604391Z'
    """
    utc = tzutc()

    if dt.tzinfo:
        dt = dt.astimezone(utc).replace(tzinfo=None)
    return dt.isoformat() + 'Z'