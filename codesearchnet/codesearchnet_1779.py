def formatdate(timeval=None):
    """Returns time format preferred for Internet standards.

    Sun, 06 Nov 1994 08:49:37 GMT  ; RFC 822, updated by RFC 1123

    According to RFC 1123, day and month names must always be in
    English.  If not for that, this code could use strftime().  It
    can't because strftime() honors the locale and could generate
    non-English names.
    """
    if timeval is None:
        timeval = time.time()
    timeval = time.gmtime(timeval)
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
            ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")[timeval[6]],
            timeval[2],
            ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")[timeval[1]-1],
                                timeval[0], timeval[3], timeval[4], timeval[5])