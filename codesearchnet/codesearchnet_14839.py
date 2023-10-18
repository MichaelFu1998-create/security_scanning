def calc_periods(hour=0, minute=0):
    """Returns a tuple of start_period and end_period.

    Assumes that the period is 24-hrs.
    Parameters:
        - `hour`: the hour from 0 to 23 when the period ends
        - `minute`: the minute from 0 to 59 when the period ends
    This method will calculate the end of the period as the closest hour/minute
    going backwards.
    It will also calculate the start of the period as the passed hour/minute
    but 24 hrs ago.
    Example, if we pass 0, 0 - we will get the events from 0:00 midnight of the
    day before yesterday until today's midnight.
    If we pass 2,0 - we will get the start time as 2am of the previous morning
    till 2am of today's morning.
    By default it's midnight.
    """
    # Calculate the time intervals in a usable form
    period_end = datetime.datetime.utcnow().replace(hour=hour,
                                                    minute=minute,
                                                    second=0,
                                                    microsecond=0)
    period_start = period_end - datetime.timedelta(days=1)

    # period end should be slightly before the midnight.
    # hence, we subtract a second
    # this will force period_end to store something like:
    # datetime.datetime(2016, 5, 19, 23, 59, 59, 999999)
    # instead of:
    # datetime.datetime(2016, 5, 20,  0,  0,  0,      0)
    period_end -= datetime.timedelta(seconds=1)

    return (period_start, period_end)