def _uptime_bsd():
    """Returns uptime in seconds or None, on BSD (including OS X)."""
    global __boottime
    try:
        libc = ctypes.CDLL('libc.so')
    except AttributeError:
        return None
    except OSError:
        # OS X; can't use ctypes.util.find_library because that creates
        # a new process on Linux, which is undesirable.
        try:
            libc = ctypes.CDLL('libc.dylib')
        except OSError:
            return None

    if not hasattr(libc, 'sysctlbyname'):
        # Not BSD.
        return None

    # Determine how much space we need for the response.
    sz = ctypes.c_uint(0)
    libc.sysctlbyname('kern.boottime', None, ctypes.byref(sz), None, 0)
    if sz.value != struct.calcsize('@LL'):
        # Unexpected, let's give up.
        return None

    # For real now.
    buf = ctypes.create_string_buffer(sz.value)
    libc.sysctlbyname('kern.boottime', buf, ctypes.byref(sz), None, 0)
    sec, usec = struct.unpack('@LL', buf.raw)

    # OS X disagrees what that second value is.
    if usec > 1000000:
        usec = 0.

    __boottime = sec + usec / 1000000.
    up = time.time() - __boottime
    if up < 0:
        up = None
    return up