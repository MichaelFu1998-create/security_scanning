def get_db_from_db(db_string):
    """Return a CouchDB database instance from a database string."""
    server = get_server_from_db(db_string)
    local_match = PLAIN_RE.match(db_string)
    remote_match = URL_RE.match(db_string)
    # If this looks like a local specifier:
    if local_match:
        return server[local_match.groupdict()['database']]
    elif remote_match:
        return server[remote_match.groupdict()['database']]
    raise ValueError('Invalid database string: %r' % (db_string,))