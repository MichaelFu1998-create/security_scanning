def compact_interval_string(value_list):
  """Compact a list of integers into a comma-separated string of intervals.

  Args:
    value_list: A list of sortable integers such as a list of numbers

  Returns:
    A compact string representation, such as "1-5,8,12-15"
  """

  if not value_list:
    return ''

  value_list.sort()

  # Start by simply building up a list of separate contiguous intervals
  interval_list = []
  curr = []
  for val in value_list:
    if curr and (val > curr[-1] + 1):
      interval_list.append((curr[0], curr[-1]))
      curr = [val]
    else:
      curr.append(val)

  if curr:
    interval_list.append((curr[0], curr[-1]))

  # For each interval collapse it down to "first, last" or just "first" if
  # if first == last.
  return ','.join([
      '{}-{}'.format(pair[0], pair[1]) if pair[0] != pair[1] else str(pair[0])
      for pair in interval_list
  ])