def _getOneMatchingRowWithRetries(self, tableInfo, fieldsToMatch,
                                    selectFieldNames):
    """ Like _getOneMatchingRowNoRetries(), but with retries on transient MySQL
    failures
    """
    with ConnectionFactory.get() as conn:
      return self._getOneMatchingRowNoRetries(tableInfo, conn, fieldsToMatch,
                                              selectFieldNames)