def _operation_status_message(self):
    """Returns the most relevant status string and last updated date string.

    This string is meant for display only.

    Returns:
      A printable status string and date string.
    """
    metadata = self._op['metadata']
    if not self._op['done']:
      if 'events' in metadata and metadata['events']:
        # Get the last event
        last_event = metadata['events'][-1]

        msg = last_event['description']
        ds = last_event['startTime']
      else:
        msg = 'Pending'
        ds = metadata['createTime']
    else:
      ds = metadata['endTime']

      if 'error' in self._op:
        msg = self._op['error']['message']
      else:
        msg = 'Success'

    return (msg, google_base.parse_rfc3339_utc_string(ds))