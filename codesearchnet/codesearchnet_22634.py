def get_or_create_db(db_name, server_url='http://127.0.0.1:5984/'):
    """Return an (optionally existing) CouchDB database instance."""
    server = get_server(server_url)
    if db_name in server:
        return server[db_name]
    return server.create(db_name)