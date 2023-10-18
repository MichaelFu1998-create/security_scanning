def get_filtered_normalized_events(self):
    """Filter the granular v2 events down to events of interest.

    Filter through the large number of granular events returned by the
    pipelines API, and extract only those that are interesting to a user. This
    is implemented by filtering out events which are known to be uninteresting
    (i.e. the default actions run for every job) and by explicitly matching
    specific events which are interesting and mapping those to v1 style naming.

    Events which are not whitelisted or blacklisted will still be output,
    meaning any events which are added in the future won't be masked.
    We don't want to suppress display of events that we don't recognize.
    They may be important.

    Returns:
      A list of maps containing the normalized, filtered events.
    """
    # Need the user-image to look for the right "pulling image" event
    user_image = google_v2_operations.get_action_image(self._op,
                                                       _ACTION_USER_COMMAND)

    # Only create an "ok" event for operations with SUCCESS status.
    need_ok = google_v2_operations.is_success(self._op)

    # Events are keyed by name for easier deletion.
    events = {}

    # Events are assumed to be ordered by timestamp (newest to oldest).
    for event in google_v2_operations.get_events(self._op):
      if self._filter(event):
        continue

      mapped, match = self._map(event)
      name = mapped['name']

      if name == 'ok':
        # If we want the "ok" event, we grab the first (most recent).
        if not need_ok or 'ok' in events:
          continue

      if name == 'pulling-image':
        if match.group(1) != user_image:
          continue

      events[name] = mapped

    return sorted(events.values(), key=operator.itemgetter('start-time'))