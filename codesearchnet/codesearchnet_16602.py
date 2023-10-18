def _uptime_syllable():
    """Returns uptime in seconds or None, on Syllable."""
    global __boottime
    try:
        __boottime = os.stat('/dev/pty/mst/pty0').st_mtime
        return time.time() - __boottime
    except (NameError, OSError):
        return None