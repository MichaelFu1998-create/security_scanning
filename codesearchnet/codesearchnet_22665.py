def timestamp(t = None, forfilename=False):
    """Returns a human-readable timestamp given a Unix timestamp 't' or
    for the current time. The Unix timestamp is the number of seconds since
    start of epoch (1970-01-01 00:00:00).
    When forfilename is True, then spaces and semicolons are replace with
    hyphens. The returned string is usable as a (part of a) filename. """

    datetimesep = ' '
    timesep     = ':'
    if forfilename:
        datetimesep = '-'
        timesep     = '-'

    return time.strftime('%Y-%m-%d' + datetimesep +
                         '%H' + timesep + '%M' + timesep + '%S',
                         time.localtime(t))