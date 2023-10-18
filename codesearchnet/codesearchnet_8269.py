def formatTime(t):
    """ Properly Format Time for permlinks
    """
    if isinstance(t, float):
        return datetime.utcfromtimestamp(t).strftime(timeFormat)
    if isinstance(t, datetime):
        return t.strftime(timeFormat)