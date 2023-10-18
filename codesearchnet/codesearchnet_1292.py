def jobSetCompleted(self, jobID, completionReason, completionMsg,
                      useConnectionID = True):
    """ Change the status on the given job to completed

    Parameters:
    ----------------------------------------------------------------
    job:                 jobID of the job to mark as completed
    completionReason:    completionReason string
    completionMsg:       completionMsg string

    useConnectionID: True if the connection id of the calling function
    must be the same as the connection that created the job. Set
    to False for hypersearch workers
    """

    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:
      query = 'UPDATE %s SET status=%%s, ' \
              '              completion_reason=%%s, ' \
              '              completion_msg=%%s, ' \
              '              end_time=UTC_TIMESTAMP(), ' \
              '              _eng_last_update_time=UTC_TIMESTAMP() ' \
              '          WHERE job_id=%%s' \
              % (self.jobsTableName,)
      sqlParams = [self.STATUS_COMPLETED, completionReason, completionMsg,
                   jobID]

      if useConnectionID:
        query += ' AND _eng_cjm_conn_id=%s'
        sqlParams.append(self._connectionID)

      result = conn.cursor.execute(query, sqlParams)

      if result != 1:
        raise RuntimeError("Tried to change the status of jobID=%s to "
                           "completed, but this job could not be found or "
                           "belongs to some other CJM" % (jobID))