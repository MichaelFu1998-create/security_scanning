def _releaseConnection(self, dbConn, cursor):
    """ Release database connection and cursor; passed as a callback to
    ConnectionWrapper
    """
    self._logger.debug("Releasing connection")

    # Close the cursor
    cursor.close()

    # ... then close the database connection
    dbConn.close()
    return