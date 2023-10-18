def parseTimestamp(s):
  """
  Parses a textual datetime format and return a Python datetime object.

  The supported format is: ``yyyy-mm-dd h:m:s.ms``

  The time component is optional.

  - hours are 00..23 (no AM/PM)
  - minutes are 00..59
  - seconds are 00..59
  - micro-seconds are 000000..999999

  :param s: (string) input time text
  :return: (datetime.datetime)
  """
  s = s.strip()
  for pattern in DATETIME_FORMATS:
    try:
      return datetime.datetime.strptime(s, pattern)
    except ValueError:
      pass
  raise ValueError('The provided timestamp %s is malformed. The supported '
                   'formats are: [%s]' % (s, ', '.join(DATETIME_FORMATS)))