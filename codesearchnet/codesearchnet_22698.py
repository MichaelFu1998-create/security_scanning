def timeago(tz=None, *args, **kwargs):
    """Return a datetime so much time ago. Takes the same arguments as timedelta()."""
    return totz(datetime.now(), tz) - timedelta(*args, **kwargs)