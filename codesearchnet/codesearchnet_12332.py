def jd_to_datetime(jd, returniso=False):
    '''This converts a UTC JD to a Python `datetime` object or ISO date string.

    Parameters
    ----------

    jd : float
        The Julian date measured at UTC.

    returniso : bool
        If False, returns a naive Python `datetime` object corresponding to
        `jd`. If True, returns the ISO format string corresponding to the date
        and time at UTC from `jd`.

    Returns
    -------

    datetime or str
        Depending on the value of `returniso`.

    '''

    tt = astime.Time(jd, format='jd', scale='utc')

    if returniso:
        return tt.iso
    else:
        return tt.datetime