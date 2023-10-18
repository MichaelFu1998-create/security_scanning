def _uptime_solaris():
    """Returns uptime in seconds or None, on Solaris."""
    global __boottime
    try:
        kstat = ctypes.CDLL('libkstat.so')
    except (AttributeError, OSError):
        return None

    # kstat doesn't have uptime, but it does have boot time.
    # Unfortunately, getting at it isn't perfectly straightforward.
    # First, let's pretend to be kstat.h

    # Constant
    KSTAT_STRLEN = 31   # According to every kstat.h I could find.

    # Data structures
    class anon_union(ctypes.Union):
        # The ``value'' union in kstat_named_t actually has a bunch more
        # members, but we're only using it for boot_time, so we only need
        # the padding and the one we're actually using.
        _fields_ = [('c', ctypes.c_char * 16),
                    ('time', ctypes.c_int)]

    class kstat_named_t(ctypes.Structure):
        _fields_ = [('name', ctypes.c_char * KSTAT_STRLEN),
                    ('data_type', ctypes.c_char),
                    ('value', anon_union)]

    # Function signatures
    kstat.kstat_open.restype = ctypes.c_void_p
    kstat.kstat_lookup.restype = ctypes.c_void_p
    kstat.kstat_lookup.argtypes = [ctypes.c_void_p,
                                   ctypes.c_char_p,
                                   ctypes.c_int,
                                   ctypes.c_char_p]
    kstat.kstat_read.restype = ctypes.c_int
    kstat.kstat_read.argtypes = [ctypes.c_void_p,
                                 ctypes.c_void_p,
                                 ctypes.c_void_p]
    kstat.kstat_data_lookup.restype = ctypes.POINTER(kstat_named_t)
    kstat.kstat_data_lookup.argtypes = [ctypes.c_void_p,
                                        ctypes.c_char_p]

    # Now, let's do something useful.

    # Initialise kstat control structure.
    kc = kstat.kstat_open()
    if not kc:
        return None

    # We're looking for unix:0:system_misc:boot_time.
    ksp = kstat.kstat_lookup(kc, 'unix', 0, 'system_misc')
    if ksp and kstat.kstat_read(kc, ksp, None) != -1:
        data = kstat.kstat_data_lookup(ksp, 'boot_time')
        if data:
            __boottime = data.contents.value.time

    # Clean-up.
    kstat.kstat_close(kc)

    if __boottime is not None:
        return time.time() - __boottime

    return None