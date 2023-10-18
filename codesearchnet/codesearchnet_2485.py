def validateInterval(self, startTime, endTime):
    """
    Helper function to validate interval.
    An interval is valid if starttime and endtime are integrals,
    and starttime is less than the endtime.
    Raises exception if interval is not valid.
    """
    start = int(startTime)
    end = int(endTime)
    if start > end:
      raise Exception("starttime is greater than endtime.")