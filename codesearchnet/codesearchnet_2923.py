def get_time_ranges(ranges):
  '''
  :param ranges:
  :return:
  '''
  # get the current time
  now = int(time.time())

  # form the new
  time_slots = dict()

  for key, value in ranges.items():
    time_slots[key] = (now - value[0], now - value[1], value[2])

  return (now, time_slots)