def jobIncrementIntField(self, jobID, fieldName, increment=1,
                           useConnectionID=False):
    """ Incremet the value of 1 field in a job by increment. The 'fieldName' is
    the public name of the field (camelBack, not the lower_case_only form as
    stored in the DB).

    This method is used for example by HypersearcWorkers to update the
    engWorkerState field periodically. By qualifying on curValue, it insures
    that only 1 worker at a time is elected to perform the next scheduled
    periodic sweep of the models.

    Parameters:
    ----------------------------------------------------------------
    jobID:        jobID of the job record to modify
    fieldName:    public field name of the field
    increment:    increment is added to the current value of the field
    """
    # Get the private field name and string form of the value
    dbFieldName = self._jobs.pubToDBNameDict[fieldName]

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:
      query = 'UPDATE %s SET %s=%s+%%s ' \
              '          WHERE job_id=%%s' \
              % (self.jobsTableName, dbFieldName, dbFieldName)
      sqlParams = [increment, jobID]

      if useConnectionID:
        query += ' AND _eng_cjm_conn_id=%s'
        sqlParams.append(self._connectionID)

      result = conn.cursor.execute(query, sqlParams)

    if result != 1:
      raise RuntimeError(
        "Tried to increment the field (%r) of jobID=%s (conn_id=%r), but an " \
        "error occurred. result=%r; query=%r" % (
          dbFieldName, jobID, self._connectionID, result, query))