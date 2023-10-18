def parse_rfc3339_utc_string(rfc3339_utc_string):
  """Converts a datestamp from RFC3339 UTC to a datetime.

  Args:
    rfc3339_utc_string: a datetime string in RFC3339 UTC "Zulu" format

  Returns:
    A datetime.
  """

  # The timestamp from the Google Operations are all in RFC3339 format, but
  # they are sometimes formatted to millisconds, microseconds, sometimes
  # nanoseconds, and sometimes only seconds:
  # * 2016-11-14T23:05:56Z
  # * 2016-11-14T23:05:56.010Z
  # * 2016-11-14T23:05:56.010429Z
  # * 2016-11-14T23:05:56.010429380Z
  m = re.match(r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2}).?(\d*)Z',
               rfc3339_utc_string)

  # It would be unexpected to get a different date format back from Google.
  # If we raise an exception here, we can break people completely.
  # Instead, let's just return None and people can report that some dates
  # are not showing up.
  # We might reconsider this approach in the future; it was originally
  # established when dates were only used for display.
  if not m:
    return None

  groups = m.groups()
  if len(groups[6]) not in (0, 3, 6, 9):
    return None

  # Create a UTC datestamp from parsed components
  # 1- Turn components 0-5 from strings to integers
  # 2- If the last component does not exist, set it to 0.
  #    If it does exist, make sure to interpret it as milliseconds.
  g = [int(val) for val in groups[:6]]

  fraction = groups[6]
  if not fraction:
    micros = 0
  elif len(fraction) == 3:
    micros = int(fraction) * 1000
  elif len(fraction) == 6:
    micros = int(fraction)
  elif len(fraction) == 9:
    # When nanoseconds are provided, we round
    micros = int(round(int(fraction) / 1000))
  else:
    assert False, 'Fraction length not 0, 6, or 9: {}'.len(fraction)

  try:
    return datetime(g[0], g[1], g[2], g[3], g[4], g[5], micros, tzinfo=pytz.utc)
  except ValueError as e:
    assert False, 'Could not parse RFC3339 datestring: {} exception: {}'.format(
        rfc3339_utc_string, e)