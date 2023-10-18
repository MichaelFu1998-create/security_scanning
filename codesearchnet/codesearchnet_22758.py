def db_to_specifier(db_string):
    """
    Return the database specifier for a database string.
    
    This accepts a database name or URL, and returns a database specifier in the
    format accepted by ``specifier_to_db``. It is recommended that you consult
    the documentation for that function for an explanation of the format.
    """
    local_match = PLAIN_RE.match(db_string)
    remote_match = URL_RE.match(db_string)
    # If this looks like a local specifier:
    if local_match:
        return 'local:' + local_match.groupdict()['database']
    # If this looks like a remote specifier:
    elif remote_match:
        # Just a fancy way of getting 3 variables in 2 lines...
        hostname, portnum, database = map(remote_match.groupdict().get,
            ('hostname', 'portnum', 'database'))
        local_url = settings._('COUCHDB_SERVER', 'http://127.0.0.1:5984/')
        localhost, localport = urlparse.urlparse(local_url)[1].split(':')
        # If it's the local server, then return a local specifier.
        if (localhost == hostname) and (localport == portnum):
            return 'local:' + database
        # Otherwise, prepare and return the remote specifier.
        return 'remote:%s:%s:%s' % (hostname, portnum, database)
    # Throw a wobbly.
    raise ValueError('Invalid database string: %r' % (db_string,))