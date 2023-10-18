def detect_timestamp_format(timestamp):
  """
  Given an input timestamp string, determine what format is it likely in.

  :param string timestamp: the timestamp string for which we need to determine format
  :return: best guess timestamp format
  """
  time_formats = {
      'epoch': re.compile(r'^[0-9]{10}$'),
      'epoch_ms': re.compile(r'^[0-9]{13}$'),
      'epoch_fraction': re.compile(r'^[0-9]{10}\.[0-9]{3,9}$'),
      '%Y-%m-%d %H:%M:%S': re.compile(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'),
      '%Y-%m-%dT%H:%M:%S': re.compile(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'),
      '%Y-%m-%d_%H:%M:%S': re.compile(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]_[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'),
      '%Y-%m-%d %H:%M:%S.%f': re.compile(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]+$'),
      '%Y-%m-%dT%H:%M:%S.%f': re.compile(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]+$'),
      '%Y-%m-%d_%H:%M:%S.%f': re.compile(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]_[0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]+$'),
      '%Y%m%d %H:%M:%S': re.compile(r'^[0-9]{4}[0-1][0-9][0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'),
      '%Y%m%dT%H:%M:%S': re.compile(r'^[0-9]{4}[0-1][0-9][0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'),
      '%Y%m%d_%H:%M:%S': re.compile(r'^[0-9]{4}[0-1][0-9][0-3][0-9]_[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'),
      '%Y%m%d %H:%M:%S.%f': re.compile(r'^[0-9]{4}[0-1][0-9][0-3][0-9] [0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]+$'),
      '%Y%m%dT%H:%M:%S.%f': re.compile(r'^[0-9]{4}[0-1][0-9][0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]+$'),
      '%Y%m%d_%H:%M:%S.%f': re.compile(r'^[0-9]{4}[0-1][0-9][0-3][0-9]_[0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]+$'),
      '%H:%M:%S': re.compile(r'^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'),
      '%H:%M:%S.%f': re.compile(r'^[0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]+$'),
      '%Y-%m-%dT%H:%M:%S.%f%z': re.compile(r'^[0-9]{4}-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9].[0-9]+[+-][0-9]{4}$')
  }
  for time_format in time_formats:
    if re.match(time_formats[time_format], timestamp):
      return time_format
  return 'unknown'