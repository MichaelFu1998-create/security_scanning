def setDefault(self, constant, start, end):
    """ set default time """
    starttime = start / 60 * 60
    if starttime < start:
      starttime += 60
    endtime = end / 60 * 60
    while starttime <= endtime:
      # STREAMCOMP-1559
      # Second check is a work around, because the response from tmaster
      # contains value 0, if it is queries for the current timestamp,
      # since the bucket is created in the tmaster, but is not filled
      # by the metrics.
      if starttime not in self.timeline or self.timeline[starttime] == 0:
        self.timeline[starttime] = constant
      starttime += 60