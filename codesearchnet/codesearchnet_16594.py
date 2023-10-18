def _uptime_linux():
    """Returns uptime in seconds or None, on Linux."""
    # With procfs
    try:
        f = open('/proc/uptime', 'r')
        up = float(f.readline().split()[0])
        f.close()
        return up
    except (IOError, ValueError):
        pass

    # Without procfs (really?)
    try:
        libc = ctypes.CDLL('libc.so')
    except AttributeError:
        return None
    except OSError:
        # Debian and derivatives do the wrong thing because /usr/lib/libc.so
        # is a GNU ld script rather than an ELF object. To get around this, we
        # have to be more specific.
        # We don't want to use ctypes.util.find_library because that creates a
        # new process on Linux. We also don't want to try too hard because at
        # this point we're already pretty sure this isn't Linux.
        try:
            libc = ctypes.CDLL('libc.so.6')
        except OSError:
            return None

    if not hasattr(libc, 'sysinfo'):
        # Not Linux.
        return None

    buf = ctypes.create_string_buffer(128) # 64 suffices on 32-bit, whatever.
    if libc.sysinfo(buf) < 0:
        return None

    up = struct.unpack_from('@l', buf.raw)[0]
    if up < 0:
        up = None
    return up