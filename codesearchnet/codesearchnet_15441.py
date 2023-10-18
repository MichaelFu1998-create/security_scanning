def create_pg_notify_event(notif):
    """A factory for creating a Postgres Notification Event
    (an object inheriting from `cnxpublishing.events.PGNotifyEvent`)
    given `notif`, a `psycopg2.extensions.Notify` object.

    """
    # TODO Lookup registered events via getAllUtilitiesRegisteredFor
    #      for class mapping.
    if notif.channel not in _CHANNEL_MAPPER:
        cls = _CHANNEL_MAPPER[None]
    else:
        cls = _CHANNEL_MAPPER[notif.channel]
    return cls(notif)