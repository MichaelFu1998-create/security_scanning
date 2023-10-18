def acquireConnection(self):
    """ Create a Connection instance.

    Parameters:
    ----------------------------------------------------------------
    retval:       A ConnectionWrapper instance. NOTE: Caller
                    is responsible for calling the  ConnectionWrapper
                    instance's release() method or use it in a context manager
                    expression (with ... as:) to release resources.
    """
    self._logger.debug("Acquiring connection")

    dbConn = SteadyDB.connect(** _getCommonSteadyDBArgsDict())
    connWrap = ConnectionWrapper(dbConn=dbConn,
                                 cursor=dbConn.cursor(),
                                 releaser=self._releaseConnection,
                                 logger=self._logger)
    return connWrap