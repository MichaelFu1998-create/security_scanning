def get_event_of_type(op, event_type):
  """Return all events of a particular type."""
  events = get_events(op)
  if not events:
    return None

  return [e for e in events if e.get('details', {}).get('@type') == event_type]