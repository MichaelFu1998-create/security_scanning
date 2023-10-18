def unixtime_to_jd(unix_time):
    '''This converts UNIX time in seconds to a Julian date in UTC (JD_UTC).

    Parameters
    ----------

    unix_time : float
        A UNIX time in decimal seconds since the 1970 UNIX epoch.

    Returns
    -------

    jd : float
        The Julian date corresponding to the provided UNIX time.

    '''

    # use astropy's time module
    jdutc = astime.Time(unix_time, format='unix', scale='utc')
    return jdutc.jd