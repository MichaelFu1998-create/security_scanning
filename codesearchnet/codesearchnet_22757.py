def specifier_to_db(db_spec):
    """
    Return the database string for a database specifier.
    
    The database specifier takes a custom format for specifying local and remote
    databases. A local database is specified by the following format:
        
        local:<db_name>
    
    For example, a database called 'sessions' would be specified by the string
    ``'local:sessions'``. Remote databases are specified like this:
    
        remote:<host>:<port_num>:<db_name>
    
    For example, a database called 'log' on the server 'dev.example.com' at port
    number 5984 would be specified by ``'remote:dev.example.com:5984:log'``.
    
    These specifiers are translated into strings acceptable to CouchDB; local
    specs are turned into the database name alone, and remote specs are turned
    into ``'http://host:port/db_name'`` URLs.
    """
    local_match = LOCAL_RE.match(db_spec)
    remote_match = REMOTE_RE.match(db_spec)
    plain_match = PLAIN_RE.match(db_spec)
    # If this looks like a local specifier:
    if local_match:
        return local_match.groupdict()['database']
    # If this looks like a remote specifier:
    elif remote_match:
        # A fancy 'unpacking'...
        hostname, portnum, database = map(remote_match.groupdict().get,
            ('hostname', 'portnum', 'database'))
        local_url = settings._('COUCHDB_SERVER', 'http://127.0.0.1:5984/')
        localhost, localport = urlparse.urlparse(local_url)[1].split(':')
        # If it's local, return a local DB string.
        if (localhost == hostname) and (localport == portnum):
            return database
        # Otherwise, get a remote URL.
        return 'http://%s:%s/%s' % (hostname, portnum, database)
    # If this looks like a plain database name, return it.
    elif plain_match:
        return plain_match.groupdict()['database']
    # Throw a wobbly.
    raise ValueError('Invalid database spec: %r' % (db_spec,))