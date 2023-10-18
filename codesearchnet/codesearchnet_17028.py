def record_view_event_builder(event, sender_app, pid=None, record=None,
                              **kwargs):
    """Build a record-view event."""
    event.update(dict(
        # When:
        timestamp=datetime.datetime.utcnow().isoformat(),
        # What:
        record_id=str(record.id),
        pid_type=pid.pid_type,
        pid_value=str(pid.pid_value),
        referrer=request.referrer,
        # Who:
        **get_user()
    ))
    return event