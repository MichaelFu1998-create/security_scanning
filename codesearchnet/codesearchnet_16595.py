def _boottime_linux():
    """A way to figure out the boot time directly on Linux."""
    global __boottime
    try:
        f = open('/proc/stat', 'r')
        for line in f:
            if line.startswith('btime'):
                __boottime = int(line.split()[1])

        if datetime is None:
            raise NotImplementedError('datetime module required.')

        return datetime.fromtimestamp(__boottime)
    except (IOError, IndexError):
        return None