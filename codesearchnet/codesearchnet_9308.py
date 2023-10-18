def _operation_status_message(self):
    """Returns the most relevant status string and failed action.

    This string is meant for display only.

    Returns:
      A printable status string and name of failed action (if any).
    """
    msg = None
    action = None
    if not google_v2_operations.is_done(self._op):
      last_event = google_v2_operations.get_last_event(self._op)
      if last_event:
        msg = last_event['description']
        action_id = last_event.get('details', {}).get('actionId')
        if action_id:
          action = google_v2_operations.get_action_by_id(self._op, action_id)
      else:
        msg = 'Pending'
    else:
      failed_events = google_v2_operations.get_failed_events(self._op)
      if failed_events:
        failed_event = failed_events[-1]
        msg = failed_event.get('details', {}).get('stderr')
        action_id = failed_event.get('details', {}).get('actionId')
        if action_id:
          action = google_v2_operations.get_action_by_id(self._op, action_id)
      if not msg:
        error = google_v2_operations.get_error(self._op)
        if error:
          msg = error['message']
        else:
          msg = 'Success'

    return msg, action