def uptime():
    """Returns uptime in seconds if even remotely possible, or None if not."""
    if __boottime is not None:
        return time.time() - __boottime

    return {'amiga': _uptime_amiga,
            'aros12': _uptime_amiga,
            'beos5': _uptime_beos,
            'cygwin': _uptime_linux,
            'darwin': _uptime_osx,
            'haiku1': _uptime_beos,
            'linux': _uptime_linux,
            'linux-armv71': _uptime_linux,
            'linux2': _uptime_linux,
            'mac': _uptime_mac,
            'minix3': _uptime_minix,
            'riscos': _uptime_riscos,
            'sunos5': _uptime_solaris,
            'syllable': _uptime_syllable,
            'win32': _uptime_windows,
            'wince': _uptime_windows}.get(sys.platform, _uptime_bsd)() or \
           _uptime_bsd() or _uptime_plan9() or _uptime_linux() or \
           _uptime_windows() or _uptime_solaris() or _uptime_beos() or \
           _uptime_amiga() or _uptime_riscos() or _uptime_posix() or \
           _uptime_syllable() or _uptime_mac() or _uptime_osx()