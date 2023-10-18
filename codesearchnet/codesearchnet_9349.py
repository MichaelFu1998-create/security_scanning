def _interval_to_seconds(interval, valid_units='smhdw'):
  """Convert the timeout duration to seconds.

  The value must be of the form "<integer><unit>" where supported
  units are s, m, h, d, w (seconds, minutes, hours, days, weeks).

  Args:
    interval: A "<integer><unit>" string.
    valid_units: A list of supported units.

  Returns:
    A string of the form "<integer>s" or None if timeout is empty.
  """
  if not interval:
    return None

  try:
    last_char = interval[-1]

    if last_char == 's' and 's' in valid_units:
      return str(float(interval[:-1])) + 's'
    elif last_char == 'm' and 'm' in valid_units:
      return str(float(interval[:-1]) * 60) + 's'
    elif last_char == 'h' and 'h' in valid_units:
      return str(float(interval[:-1]) * 60 * 60) + 's'
    elif last_char == 'd' and 'd' in valid_units:
      return str(float(interval[:-1]) * 60 * 60 * 24) + 's'
    elif last_char == 'w' and 'w' in valid_units:
      return str(float(interval[:-1]) * 60 * 60 * 24 * 7) + 's'
    else:
      raise ValueError(
          'Unsupported units in interval string %s: %s' % (interval, last_char))

  except (ValueError, OverflowError) as e:
    raise ValueError('Unable to parse interval string %s: %s' % (interval, e))