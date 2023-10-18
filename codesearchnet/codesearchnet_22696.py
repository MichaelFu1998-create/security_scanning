def to_datetime(when):
    """
    Convert a date or time to a datetime. If when is a date then it sets the time to midnight. If
    when is a time it sets the date to the epoch. If when is None or a datetime it returns when.
    Otherwise a TypeError is raised. Returned datetimes have tzinfo set to None unless when is a
    datetime with tzinfo set in which case it remains the same.
    """
    if when is None or is_datetime(when):
        return when
    if is_time(when):
        return datetime.combine(epoch.date(), when)
    if is_date(when):
        return datetime.combine(when, time(0))
    raise TypeError("unable to convert {} to datetime".format(when.__class__.__name__))