def _createDefaultPolicy(cls):
    """ [private] Create the default database connection policy instance

    Parameters:
    ----------------------------------------------------------------
    retval:            The default database connection policy instance
    """
    logger = _getLogger(cls)

    logger.debug(
      "Creating database connection policy: platform=%r; pymysql.VERSION=%r",
      platform.system(), pymysql.VERSION)

    if platform.system() == "Java":
      # NOTE: PooledDB doesn't seem to work under Jython
      # NOTE: not appropriate for multi-threaded applications.
      # TODO: this was fixed in Webware DBUtils r8228, so once
      #       we pick up a realease with this fix, we should use
      #       PooledConnectionPolicy for both Jython and Python.
      policy = SingleSharedConnectionPolicy()
    else:
      policy = PooledConnectionPolicy()

    return policy