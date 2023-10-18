def _getEndTime(self, t):
    """Add the aggregation period to the input time t and return a datetime object

    Years and months are handled as aspecial case due to leap years
    and months with different number of dates. They can't be converted
    to a strict timedelta because a period of 3 months will have different
    durations actually. The solution is to just add the years and months
    fields directly to the current time.

    Other periods are converted to timedelta and just added to current time.
    """

    assert isinstance(t, datetime.datetime)
    if self._aggTimeDelta:
      return t + self._aggTimeDelta
    else:
      year = t.year + self._aggYears + (t.month - 1 + self._aggMonths) / 12
      month = (t.month - 1 + self._aggMonths) % 12 + 1
      return t.replace(year=year, month=month)