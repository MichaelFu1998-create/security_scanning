def _timestamp(when):
    """
    Python 2 compatibility for `datetime.timestamp()`.
    """
    return (time.mktime(when.timetuple()) if sys.version_info < (3,) else
            when.timestamp())