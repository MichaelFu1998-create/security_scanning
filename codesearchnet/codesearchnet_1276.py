def _resumeJobNoRetries(self, conn, jobID, alreadyRunning):
    """ Resumes processing of an existing job that is presently in the
    STATUS_COMPLETED state.

    NOTE: this is primarily for resuming suspended Production and Stream Jobs; DO
     NOT use it on Hypersearch jobs.

    This prepares an existing job entry to resume processing. The CJM is always
    periodically sweeping the jobs table and when it finds a job that is ready
    to run, it will proceed to start it up on Hadoop.

    Parameters:
    ----------------------------------------------------------------
    conn:            Owned connection acquired from ConnectionFactory.get()
    jobID:          jobID of the job to resume
    alreadyRunning: Used for unit test purposes only. This inserts the job
                     in the running state. It is used when running a worker
                     in standalone mode without hadoop.

    raises:         Throws a RuntimeError if no rows are affected. This could
                    either be because:
                      1) Because there was not matching jobID
                      2) or if the status of the job was not STATUS_COMPLETED.

    retval:            nothing
    """

    # Initial status
    if alreadyRunning:
      # Use STATUS_TESTMODE so scheduler will leave our row alone
      initStatus = self.STATUS_TESTMODE
    else:
      initStatus = self.STATUS_NOTSTARTED

    # NOTE: some of our clients (e.g., StreamMgr) may call us (directly or
    #  indirectly) for the same job from different processes (even different
    #  machines), so we should be prepared for the update to fail; same holds
    #  if the UPDATE succeeds, but connection fails while reading result
    assignments = [
      'status=%s',
      'completion_reason=DEFAULT',
      'completion_msg=DEFAULT',
      'worker_completion_reason=DEFAULT',
      'worker_completion_msg=DEFAULT',
      'end_time=DEFAULT',
      'cancel=DEFAULT',
      '_eng_last_update_time=UTC_TIMESTAMP()',
      '_eng_allocate_new_workers=DEFAULT',
      '_eng_untended_dead_workers=DEFAULT',
      'num_failed_workers=DEFAULT',
      'last_failed_worker_error_msg=DEFAULT',
      '_eng_cleaning_status=DEFAULT',
    ]
    assignmentValues = [initStatus]

    if alreadyRunning:
      assignments += ['_eng_cjm_conn_id=%s', 'start_time=UTC_TIMESTAMP()',
                      '_eng_last_update_time=UTC_TIMESTAMP()']
      assignmentValues.append(self._connectionID)
    else:
      assignments += ['_eng_cjm_conn_id=DEFAULT', 'start_time=DEFAULT']

    assignments = ', '.join(assignments)

    query = 'UPDATE %s SET %s ' \
              '          WHERE job_id=%%s AND status=%%s' \
              % (self.jobsTableName, assignments)
    sqlParams = assignmentValues + [jobID, self.STATUS_COMPLETED]

    numRowsAffected = conn.cursor.execute(query, sqlParams)

    assert numRowsAffected <= 1, repr(numRowsAffected)

    if numRowsAffected == 0:
      self._logger.info(
        "_resumeJobNoRetries: Redundant job-resume UPDATE: job was not "
        "suspended or was resumed by another process or operation was retried "
        "after connection failure; jobID=%s", jobID)

    return