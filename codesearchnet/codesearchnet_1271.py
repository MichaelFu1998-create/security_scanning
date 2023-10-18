def _getMatchingRowsNoRetries(self, tableInfo, conn, fieldsToMatch,
                                selectFieldNames, maxRows=None):
    """ Return a sequence of matching rows with the requested field values from
    a table or empty sequence if nothing matched.

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
    maxRows:         maximum number of rows to return; unlimited if maxRows
                      is None

    retval:          A sequence of matching rows, each row consisting of field
                      values in the order of the requested field names.  Empty
                      sequence is returned when not match exists.
    """

    assert fieldsToMatch, repr(fieldsToMatch)
    assert all(k in tableInfo.dbFieldNames
               for k in fieldsToMatch.iterkeys()), repr(fieldsToMatch)

    assert selectFieldNames, repr(selectFieldNames)
    assert all(f in tableInfo.dbFieldNames for f in selectFieldNames), repr(
      selectFieldNames)

    # NOTE: make sure match expressions and values are in the same order
    matchPairs = fieldsToMatch.items()
    matchExpressionGen = (
      p[0] +
      (' IS ' + {True:'TRUE', False:'FALSE'}[p[1]] if isinstance(p[1], bool)
       else ' IS NULL' if p[1] is None
       else ' IN %s' if isinstance(p[1], self._SEQUENCE_TYPES)
       else '=%s')
      for p in matchPairs)
    matchFieldValues = [p[1] for p in matchPairs
                        if (not isinstance(p[1], (bool)) and p[1] is not None)]

    query = 'SELECT %s FROM %s WHERE (%s)' % (
      ','.join(selectFieldNames), tableInfo.tableName,
      ' AND '.join(matchExpressionGen))
    sqlParams = matchFieldValues
    if maxRows is not None:
      query += ' LIMIT %s'
      sqlParams.append(maxRows)

    conn.cursor.execute(query, sqlParams)
    rows = conn.cursor.fetchall()

    if rows:
      assert maxRows is None or len(rows) <= maxRows, "%d !<= %d" % (
        len(rows), maxRows)
      assert len(rows[0]) == len(selectFieldNames), "%d != %d" % (
        len(rows[0]), len(selectFieldNames))
    else:
      rows = tuple()

    return rows