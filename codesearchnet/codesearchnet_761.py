def get(cls):
    """ Acquire a ConnectionWrapper instance that represents a connection
    to the SQL server per nupic.cluster.database.* configuration settings.

    NOTE: caller is responsible for calling the ConnectionWrapper instance's
    release() method after using the connection in order to release resources.
    Better yet, use the returned ConnectionWrapper instance in a Context Manager
    statement for automatic invocation of release():
    Example:
        # If using Jython 2.5.x, first import with_statement at the very top of
        your script (don't need this import for Jython/Python 2.6.x and later):
        from __future__ import with_statement
        # Then:
        from nupic.database.Connection import ConnectionFactory
        # Then use it like this
        with ConnectionFactory.get() as conn:
          conn.cursor.execute("SELECT ...")
          conn.cursor.fetchall()
          conn.cursor.execute("INSERT ...")

    WARNING: DO NOT close the underlying connection or cursor as it may be
    shared by other modules in your process.  ConnectionWrapper's release()
    method will do the right thing.

    Parameters:
    ----------------------------------------------------------------
    retval:       A ConnectionWrapper instance. NOTE: Caller is responsible
                    for releasing resources as described above.
    """
    if cls._connectionPolicy is None:
      logger = _getLogger(cls)
      logger.info("Creating db connection policy via provider %r",
                  cls._connectionPolicyInstanceProvider)
      cls._connectionPolicy = cls._connectionPolicyInstanceProvider()

      logger.debug("Created connection policy: %r", cls._connectionPolicy)

    return cls._connectionPolicy.acquireConnection()