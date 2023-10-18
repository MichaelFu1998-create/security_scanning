def _computeTimestampRecordIdx(self, recordTS):
    """ Give the timestamp of a record (a datetime object), compute the record's
    timestamp index - this is the timestamp divided by the aggregation period.


    Parameters:
    ------------------------------------------------------------------------
    recordTS:  datetime instance
    retval:    record timestamp index, or None if no aggregation period
    """

    if self._aggregationPeriod is None:
      return None

    # Base record index on number of elapsed months if aggregation is in
    #  months
    if self._aggregationPeriod['months'] > 0:
      assert self._aggregationPeriod['seconds'] == 0
      result = int(
        (recordTS.year * 12 + (recordTS.month-1)) /
        self._aggregationPeriod['months'])

    # Base record index on elapsed seconds
    elif self._aggregationPeriod['seconds'] > 0:
      delta = recordTS - datetime.datetime(year=1, month=1, day=1)
      deltaSecs = delta.days * 24 * 60 * 60   \
                + delta.seconds               \
                + delta.microseconds / 1000000.0
      result = int(deltaSecs / self._aggregationPeriod['seconds'])

    else:
      result = None

    return result