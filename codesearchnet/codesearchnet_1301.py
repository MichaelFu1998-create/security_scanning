def jobSetFields(self, jobID, fields, useConnectionID=True,
                   ignoreUnchanged=False):
    """ Change the values of 1 or more fields in a job. Here, 'fields' is a
    dict with the name/value pairs to change. The names are the public names of
    the fields (camelBack, not the lower_case_only form as stored in the DB).
    This method is for private use by the ClientJobManager only.

    Parameters:
    ----------------------------------------------------------------
    jobID:     jobID of the job record

    fields:    dictionary of fields to change

    useConnectionID: True if the connection id of the calling function
    must be the same as the connection that created the job. Set
    to False for hypersearch workers

    ignoreUnchanged: The default behavior is to throw a
    RuntimeError if no rows are affected. This could either be
    because:
      1) Because there was not matching jobID
      2) or if the data to update matched the data in the DB exactly.

    Set this parameter to True if you expect case 2 and wish to
    supress the error.
    """

    # Form the sequecce of key=value strings that will go into the
    #  request
    assignmentExpressions = ','.join(
      ["%s=%%s" % (self._jobs.pubToDBNameDict[f],) for f in fields.iterkeys()])
    assignmentValues = fields.values()

    query = 'UPDATE %s SET %s ' \
            '          WHERE job_id=%%s' \
            % (self.jobsTableName, assignmentExpressions,)
    sqlParams = assignmentValues + [jobID]

    if useConnectionID:
      query += ' AND _eng_cjm_conn_id=%s'
      sqlParams.append(self._connectionID)

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:
      result = conn.cursor.execute(query, sqlParams)

    if result != 1 and not ignoreUnchanged:
      raise RuntimeError(
        "Tried to change fields (%r) of jobID=%s conn_id=%r), but an error " \
        "occurred. result=%r; query=%r" % (
          assignmentExpressions, jobID, self._connectionID, result, query))