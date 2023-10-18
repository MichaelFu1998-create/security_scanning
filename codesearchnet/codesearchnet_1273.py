def _getOneMatchingRowNoRetries(self, tableInfo, conn, fieldsToMatch,
                                  selectFieldNames):
    """ Return a single matching row with the requested field values from the
    the requested table or None if nothing matched.

    tableInfo:       Table information: a ClientJobsDAO._TableInfoBase  instance
    conn:            Owned connection acquired from ConnectionFactory.get()
    fieldsToMatch:   Dictionary of internal fieldName/value mappings that
                     identify the desired rows. If a value is an instance of
                     ClientJobsDAO._SEQUENCE_TYPES (list/set/tuple), then the
                     operator 'IN' will be used in the corresponding SQL
                     predicate; if the value is bool: "IS TRUE/FALSE"; if the
                     value is None: "IS NULL"; '=' will be used for all other
                     cases.
    selectFieldNames:
                     list of fields to return, using internal field names

    retval:          A sequence of field values of the matching row in the order
                      of the given field names; or None if there was no match.
    """
    rows = self._getMatchingRowsNoRetries(tableInfo, conn, fieldsToMatch,
                                          selectFieldNames, maxRows=1)
    if rows:
      assert len(rows) == 1, repr(len(rows))
      result = rows[0]
    else:
      result = None

    return result