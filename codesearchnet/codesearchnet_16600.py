def _uptime_plan9():
    """Returns uptime in seconds or None, on Plan 9."""
    # Apparently Plan 9 only has Python 2.2, which I'm not prepared to
    # support. Maybe some Linuxes implement /dev/time, though, someone was
    # talking about it somewhere.
    try:
        # The time file holds one 32-bit number representing the sec-
        # onds since start of epoch and three 64-bit numbers, repre-
        # senting nanoseconds since start of epoch, clock ticks, and
        # clock frequency.
        #  -- cons(3)
        f = open('/dev/time', 'r')
        s, ns, ct, cf = f.read().split()
        f.close()
        return float(ct) / float(cf)
    except (IOError, ValueError):
        return None