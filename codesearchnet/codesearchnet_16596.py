def _uptime_amiga():
    """Returns uptime in seconds or None, on AmigaOS."""
    global __boottime
    try:
        __boottime = os.stat('RAM:').st_ctime
        return time.time() - __boottime
    except (NameError, OSError):
        return None