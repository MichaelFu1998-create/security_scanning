def _getMatchingRowsWithRetries(self, tableInfo, fieldsToMatch,
                                  selectFieldNames, maxRows=None):
    """ Like _getMatchingRowsNoRetries(), but with retries on transient MySQL
    failures
    """
    with ConnectionFactory.get() as conn:
      return self._getMatchingRowsNoRetries(tableInfo, conn, fieldsToMatch,
                                            selectFieldNames, maxRows)