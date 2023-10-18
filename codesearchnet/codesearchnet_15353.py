def processor():  # pragma: no cover
    """Churns over PostgreSQL notifications on configured channels.
    This requires the application be setup and the registry be available.
    This function uses the database connection string and a list of
    pre configured channels.

    """
    registry = get_current_registry()
    settings = registry.settings
    connection_string = settings[CONNECTION_STRING]
    channels = _get_channels(settings)

    # Code adapted from
    # http://initd.org/psycopg/docs/advanced.html#asynchronous-notifications
    with psycopg2.connect(connection_string) as conn:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with conn.cursor() as cursor:
            for channel in channels:
                cursor.execute('LISTEN {}'.format(channel))
                logger.debug('Waiting for notifications on channel "{}"'
                             .format(channel))

        registry.notify(ChannelProcessingStartUpEvent())

        rlist = [conn]  # wait until ready for reading
        wlist = []  # wait until ready for writing
        xlist = []  # wait for an "exceptional condition"
        timeout = 5

        while True:
            if select.select(rlist, wlist, xlist, timeout) != ([], [], []):
                conn.poll()
                while conn.notifies:
                    notif = conn.notifies.pop(0)
                    logger.debug('Got NOTIFY: pid={} channel={} payload={}'
                                 .format(notif.pid, notif.channel,
                                         notif.payload))
                    event = create_pg_notify_event(notif)
                    try:
                        registry.notify(event)
                    except Exception:
                        logger.exception('Logging an uncaught exception')