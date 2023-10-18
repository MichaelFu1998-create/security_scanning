def get_failed_events(op):
  """Return the events (if any) with a non-zero exitStatus."""
  events = get_events(op)
  if events:
    return [
        e for e in events if int(e.get('details', {}).get('exitStatus', 0)) != 0
    ]
  return None