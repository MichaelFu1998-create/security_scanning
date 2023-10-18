def acquireConnection(self):
    """ Get a Connection instance.

    Parameters:
    ----------------------------------------------------------------
    retval:       A ConnectionWrapper instance. NOTE: Caller
                    is responsible for calling the  ConnectionWrapper
                    instance's release() method or use it in a context manager
                    expression (with ... as:) to release resources.
    """
    self._logger.debug("Acquiring connection")

    # Check connection and attempt to re-establish it if it died (this is
    #   what PooledDB does)
    self._conn._ping_check()
    connWrap = ConnectionWrapper(dbConn=self._conn,
                                 cursor=self._conn.cursor(),
                                 releaser=self._releaseConnection,
                                 logger=self._logger)
    return connWrap