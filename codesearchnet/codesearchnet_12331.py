def datetime_to_jd(dt):
    '''This converts a Python datetime object (naive, time in UT) to JD_UTC.

    Parameters
    ----------

    dt : datetime
        A naive Python `datetime` object (e.g. with no tz attribute) measured at
        UTC.

    Returns
    -------

    jd : float
        The Julian date corresponding to the `datetime` object.

    '''

    jdutc = astime.Time(dt, format='datetime',scale='utc')
    return jdutc.jd