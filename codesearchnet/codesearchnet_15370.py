def db_connect(connection_string=None, **kwargs):
    """Function to supply a database connection object."""
    if connection_string is None:
        connection_string = get_current_registry().settings[CONNECTION_STRING]
    db_conn = psycopg2.connect(connection_string, **kwargs)
    try:
        with db_conn:
            yield db_conn
    finally:
        db_conn.close()