def isodate(datestamp=None, microseconds=False):
    """Return current or given time formatted according to ISO-8601."""
    datestamp = datestamp or datetime.datetime.now()
    if not microseconds:
        usecs = datetime.timedelta(microseconds=datestamp.microsecond)
        datestamp = datestamp - usecs
    return datestamp.isoformat(b' ' if PY2 else u' ')