def floorTimestamps(self, start, end, timeline):
    """ floor timestamp """
    ret = {}
    for timestamp, value in timeline.items():
      ts = timestamp / 60 * 60
      if start <= ts <= end:
        ret[ts] = value
    return ret