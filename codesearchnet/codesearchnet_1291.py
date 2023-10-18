def jobSetStatus(self, jobID, status, useConnectionID=True,):
    """ Change the status on the given job

    Parameters:
    ----------------------------------------------------------------
    job:        jobID of the job to change status
    status:     new status string (ClientJobsDAO.STATUS_xxxxx)

    useConnectionID: True if the connection id of the calling function
    must be the same as the connection that created the job. Set
    to False for hypersearch workers
    """
    # Get a database connection and cursor
    with ConnectionFactory.get() as conn:
      query = 'UPDATE %s SET status=%%s, ' \
              '              _eng_last_update_time=UTC_TIMESTAMP() ' \
              '          WHERE job_id=%%s' \
              % (self.jobsTableName,)
      sqlParams = [status, jobID]

      if useConnectionID:
        query += ' AND _eng_cjm_conn_id=%s'
        sqlParams.append(self._connectionID)

      result = conn.cursor.execute(query, sqlParams)

      if result != 1:
        raise RuntimeError("Tried to change the status of job %d to %s, but "
                           "this job belongs to some other CJM" % (
                            jobID, status))