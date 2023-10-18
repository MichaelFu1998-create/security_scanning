def set_connection(host=None, database=None, user=None, password=None):
    """Set connection parameters. Call set_connection with no arguments to clear."""
    c.CONNECTION['HOST'] = host
    c.CONNECTION['DATABASE'] = database
    c.CONNECTION['USER'] = user
    c.CONNECTION['PASSWORD'] = password