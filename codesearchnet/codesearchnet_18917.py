def __round_time(self, dt):
    """Round a datetime object to a multiple of a timedelta
    dt : datetime.datetime object, default now.
    """
    round_to = self._resolution.total_seconds()
    seconds  = (dt - dt.min).seconds
    rounding = (seconds + round_to / 2) // round_to * round_to
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)