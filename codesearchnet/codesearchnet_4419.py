def dbm_starter(priority_msgs, resource_msgs, *args, **kwargs):
    """Start the database manager process

    The DFK should start this function. The args, kwargs match that of the monitoring config

    """
    dbm = DatabaseManager(*args, **kwargs)
    dbm.start(priority_msgs, resource_msgs)