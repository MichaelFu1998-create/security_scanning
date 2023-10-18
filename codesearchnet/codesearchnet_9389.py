def get_last_update(op):
  """Return the most recent timestamp in the operation."""
  last_update = get_end_time(op)

  if not last_update:
    last_event = get_last_event(op)
    if last_event:
      last_update = last_event['timestamp']

  if not last_update:
    last_update = get_create_time(op)

  return last_update