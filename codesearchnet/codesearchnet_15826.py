def get_aggregation_timestamp(self, timestamp, granularity='second'):
    """
    Return a timestamp from the raw epoch time based on the granularity preferences passed in.

    :param string timestamp: timestamp from the log line
    :param string granularity: aggregation granularity used for plots.
    :return: string aggregate_timestamp: timestamp used for metrics aggregation in all functions
    """
    if granularity is None or granularity.lower() == 'none':
      return int(timestamp), 1
    elif granularity == 'hour':
      return (int(timestamp) / (3600 * 1000)) * 3600 * 1000, 3600
    elif granularity == 'minute':
      return (int(timestamp) / (60 * 1000)) * 60 * 1000, 60
    else:
      return (int(timestamp) / 1000) * 1000, 1