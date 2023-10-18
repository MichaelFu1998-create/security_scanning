def _startJobWithRetries(self, jobID):
    """ Place the given job in STATUS_RUNNING mode; the job is expected to be
    STATUS_NOTSTARTED.

    NOTE: this function was factored out of jobStartNext because it's also
     needed for testing (e.g., test_client_jobs_dao.py)
    """
    with ConnectionFactory.get() as conn:
      query = 'UPDATE %s SET status=%%s, ' \
                '            _eng_cjm_conn_id=%%s, ' \
                '            start_time=UTC_TIMESTAMP(), ' \
                '            _eng_last_update_time=UTC_TIMESTAMP() ' \
                '          WHERE (job_id=%%s AND status=%%s)' \
                % (self.jobsTableName,)
      sqlParams = [self.STATUS_RUNNING, self._connectionID,
                   jobID, self.STATUS_NOTSTARTED]
      numRowsUpdated = conn.cursor.execute(query, sqlParams)
      if numRowsUpdated != 1:
        self._logger.warn('jobStartNext: numRowsUpdated=%r instead of 1; '
                          'likely side-effect of transient connection '
                          'failure', numRowsUpdated)
    return