def _map(self, event):
    """Extract elements from an operation event and map to a named event."""
    description = event.get('description', '')
    start_time = google_base.parse_rfc3339_utc_string(
        event.get('timestamp', ''))

    for name, regex in _EVENT_REGEX_MAP.items():
      match = regex.match(description)
      if match:
        return {'name': name, 'start-time': start_time}, match

    return {'name': description, 'start-time': start_time}, None