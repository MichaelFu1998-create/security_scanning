def ensure_specifier_exists(db_spec):
    """Make sure a DB specifier exists, creating it if necessary."""
    local_match = LOCAL_RE.match(db_spec)
    remote_match = REMOTE_RE.match(db_spec)
    plain_match = PLAIN_RE.match(db_spec)
    if local_match:
        db_name = local_match.groupdict().get('database')
        server = shortcuts.get_server()
        if db_name not in server:
            server.create(db_name)
        return True
    elif remote_match:
        hostname, portnum, database = map(remote_match.groupdict().get,
            ('hostname', 'portnum', 'database'))
        server = shortcuts.get_server(
            server_url=('http://%s:%s' % (hostname, portnum)))
        if database not in server:
            server.create(database)
        return True
    elif plain_match:
        db_name = plain_match.groupdict().get('database')
        server = shortcuts.get_server()
        if db_name not in server:
            server.create(db_name)
        return True
    return False