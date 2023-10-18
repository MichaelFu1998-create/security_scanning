def boottime():
    """Returns boot time if remotely possible, or None if not."""
    global __boottime

    if __boottime is None:
        up = uptime()
        if up is None:
            return None
    if __boottime is None:
        _boottime_linux()

    if datetime is None:
        raise RuntimeError('datetime module required.')

    return datetime.fromtimestamp(__boottime or time.time() - up)