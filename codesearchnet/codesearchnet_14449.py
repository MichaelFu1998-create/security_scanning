def format_timedelta(td_object):
    """Format a timedelta object for display to users

    Returns
    -------
    str
    """
    def get_total_seconds(td):
        # timedelta.total_seconds not in py2.6
        return (td.microseconds +
                (td.seconds + td.days * 24 * 3600) * 1e6) / 1e6

    seconds = int(get_total_seconds(td_object))
    periods = [('year',    60*60*24*365),
               ('month',   60*60*24*30),
               ('day',     60*60*24),
               ('hour',    60*60),
               ('minute',  60),
               ('second',  1)]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 1:
                strings.append("%s %s" % (period_value, period_name))
            else:
                strings.append("%s %ss" % (period_value, period_name))

    return ", ".join(strings)