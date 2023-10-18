def from_timestamp(ts):
    """
    Convert a numeric timestamp to a timezone-aware datetime.

    A client may override this function to change the default behavior,
    such as to use local time or timezone-naïve times.
    """
    return datetime.datetime.utcfromtimestamp(ts).replace(tzinfo=pytz.utc)