def age_to_create_time(age, from_time=None):
  """Compute the create time (UTC) for the list filter.

  If the age is an integer value it is treated as a UTC date.
  Otherwise the value must be of the form "<integer><unit>" where supported
  units are s, m, h, d, w (seconds, minutes, hours, days, weeks).

  Args:
    age: A "<integer><unit>" string or integer value.
    from_time:

  Returns:
    A timezone-aware datetime or None if age parameter is empty.
  """

  if not age:
    return None

  if not from_time:
    from_time = dsub_util.replace_timezone(datetime.datetime.now(), tzlocal())

  try:
    last_char = age[-1]

    if last_char == 's':
      return from_time - datetime.timedelta(seconds=int(age[:-1]))
    elif last_char == 'm':
      return from_time - datetime.timedelta(minutes=int(age[:-1]))
    elif last_char == 'h':
      return from_time - datetime.timedelta(hours=int(age[:-1]))
    elif last_char == 'd':
      return from_time - datetime.timedelta(days=int(age[:-1]))
    elif last_char == 'w':
      return from_time - datetime.timedelta(weeks=int(age[:-1]))
    else:
      # If no unit is given treat the age as seconds from epoch, otherwise apply
      # the correct time unit.
      return dsub_util.replace_timezone(
          datetime.datetime.utcfromtimestamp(int(age)), pytz.utc)

  except (ValueError, OverflowError) as e:
    raise ValueError('Unable to parse age string %s: %s' % (age, e))