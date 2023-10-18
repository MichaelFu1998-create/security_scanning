def acquireConnection(self):
    """ Get a connection from the pool.

    Parameters:
    ----------------------------------------------------------------
    retval:       A ConnectionWrapper instance. NOTE: Caller
                    is responsible for calling the  ConnectionWrapper
                    instance's release() method or use it in a context manager
                    expression (with ... as:) to release resources.
    """
    self._logger.debug("Acquiring connection")

    dbConn = self._pool.connection(shareable=False)
    connWrap = ConnectionWrapper(dbConn=dbConn,
                                 cursor=dbConn.cursor(),
                                 releaser=self._releaseConnection,
                                 logger=self._logger)
    return connWrap