def _uptime_minix():
    """Returns uptime in seconds or None, on MINIX."""
    try:
        f = open('/proc/uptime', 'r')
        up = float(f.read())
        f.close()
        return up
    except (IOError, ValueError):
        return None