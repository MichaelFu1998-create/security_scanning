def jobInsertUnique(self, client, cmdLine, jobHash, clientInfo='',
                      clientKey='', params='', minimumWorkers=0,
                      maximumWorkers=0, jobType='',
                      priority=DEFAULT_JOB_PRIORITY):
    """ Add an entry to the jobs table for a new job request, but only if the
    same job, by the same client is not already running. If the job is already
    running, or queued up to run, this call does nothing. If the job does not
    exist in the jobs table or has completed, it will be inserted and/or started
    up again.

    This method is called by clients, like StreamMgr, that wish to only start up
    a job if it hasn't already been started up.

    Parameters:
    ----------------------------------------------------------------
    client:          Name of the client submitting the job
    cmdLine:         Command line to use to launch each worker process; must be
                      a non-empty string
    jobHash:         unique hash of this job. The client must insure that this
                      uniquely identifies this job request for the purposes
                      of detecting duplicates.
    clientInfo:      JSON encoded dict of client specific information.
    clientKey:       Foreign key.
    params:          JSON encoded dict of the parameters for the job. This
                      can be fetched out of the database by the worker processes
                      based on the jobID.
    minimumWorkers:  minimum number of workers design at a time.
    maximumWorkers:  maximum number of workers desired at a time.
    jobType:         The type of job that this is. This should be one of the
                      JOB_TYPE_XXXX enums. This is needed to allow a standard
                      way of recognizing a job's function and capabilities.
    priority:        Job scheduling priority; 0 is the default priority (
                      ClientJobsDAO.DEFAULT_JOB_PRIORITY); positive values are
                      higher priority (up to ClientJobsDAO.MAX_JOB_PRIORITY),
                      and negative values are lower priority (down to
                      ClientJobsDAO.MIN_JOB_PRIORITY). Higher-priority jobs will
                      be scheduled to run at the expense of the lower-priority
                      jobs, and higher-priority job tasks will preempt those
                      with lower priority if there is inadequate supply of
                      scheduling slots. Excess lower priority job tasks will
                      starve as long as slot demand exceeds supply. Most jobs
                      should be scheduled with DEFAULT_JOB_PRIORITY. System jobs
                      that must run at all cost, such as Multi-Model-Master,
                      should be scheduled with MAX_JOB_PRIORITY.

    retval:          jobID of the newly inserted or existing job.
    """

    assert cmdLine, "Unexpected empty or None command-line: " + repr(cmdLine)

    @g_retrySQL
    def insertUniqueWithRetries():
      jobHashValue = self._normalizeHash(jobHash)

      jobID = None
      with ConnectionFactory.get() as conn:
        row = self._getOneMatchingRowNoRetries(
          self._jobs, conn, dict(client=client, job_hash=jobHashValue),
          ['job_id', 'status'])

        if row is not None:
          (jobID, status) = row

          if status == self.STATUS_COMPLETED:
            # Restart existing job that had completed
            query = 'UPDATE %s SET client_info=%%s, ' \
                    '              client_key=%%s, ' \
                    '              cmd_line=%%s, ' \
                    '              params=%%s, ' \
                    '              minimum_workers=%%s, ' \
                    '              maximum_workers=%%s, ' \
                    '              priority=%%s, '\
                    '              _eng_job_type=%%s ' \
                    '          WHERE (job_id=%%s AND status=%%s)' \
                    % (self.jobsTableName,)
            sqlParams = (clientInfo, clientKey, cmdLine, params,
                         minimumWorkers, maximumWorkers, priority,
                         jobType, jobID, self.STATUS_COMPLETED)

            numRowsUpdated = conn.cursor.execute(query, sqlParams)
            assert numRowsUpdated <= 1, repr(numRowsUpdated)

            if numRowsUpdated == 0:
              self._logger.info(
                "jobInsertUnique: Redundant job-reuse UPDATE: job restarted by "
                "another process, values were unchanged, or operation was "
                "retried after connection failure; jobID=%s", jobID)

            # Restart the job, unless another process beats us to it
            self._resumeJobNoRetries(conn, jobID, alreadyRunning=False)
        else:
          # There was no job row with matching client/jobHash, so insert one
          jobID = self._insertOrGetUniqueJobNoRetries(
            conn, client=client, cmdLine=cmdLine, jobHash=jobHashValue,
            clientInfo=clientInfo, clientKey=clientKey, params=params,
            minimumWorkers=minimumWorkers, maximumWorkers=maximumWorkers,
            jobType=jobType, priority=priority, alreadyRunning=False)

        return jobID

    try:
      jobID = insertUniqueWithRetries()
    except:
      self._logger.exception(
        'jobInsertUnique FAILED: jobType=%r; client=%r; '
        'clientInfo=%r; clientKey=%r; jobHash=%r; cmdLine=%r',
        jobType, client, _abbreviate(clientInfo, 48), clientKey, jobHash,
        cmdLine)
      raise
    else:
      self._logger.info(
        'jobInsertUnique: returning jobID=%s. jobType=%r; client=%r; '
        'clientInfo=%r; clientKey=%r; jobHash=%r; cmdLine=%r',
        jobID, jobType, client, _abbreviate(clientInfo, 48), clientKey,
        jobHash, cmdLine)

    return jobID