def _format_iso_time(self, time):
    """Makes sure we have proper ISO 8601 time.

    :param time: either already ISO 8601 a string or datetime.datetime
    :returns: ISO 8601 time
    :rtype: str

    """
    if isinstance(time, str):
      return time
    elif isinstance(time, datetime):
      return time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    else:
      return None