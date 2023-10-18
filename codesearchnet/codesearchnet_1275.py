def _insertOrGetUniqueJobNoRetries(
    self, conn, client, cmdLine, jobHash, clientInfo, clientKey, params,
    minimumWorkers, maximumWorkers, jobType, priority, alreadyRunning):
    """ Attempt to insert a row with the given parameters into the jobs table.
    Return jobID of the inserted row, or of an existing row with matching
    client/jobHash key.

    The combination of client and jobHash are expected to be unique (enforced
    by a unique index on the two columns).

    NOTE: It's possibe that this or another process (on this or another machine)
     already inserted a row with matching client/jobHash key (e.g.,
     StreamMgr). This may also happen undetected by this function due to a
     partially-successful insert operation (e.g., row inserted, but then
     connection was lost while reading response) followed by retries either of
     this function or in SteadyDB module.

    Parameters:
    ----------------------------------------------------------------
    conn:            Owned connection acquired from ConnectionFactory.get()
    client:          Name of the client submitting the job
    cmdLine:         Command line to use to launch each worker process; must be
                      a non-empty string
    jobHash:         unique hash of this job. The caller must insure that this,
                      together with client, uniquely identifies this job request
                      for the purposes of detecting duplicates.
    clientInfo:      JSON encoded dict of client specific information.
    clientKey:       Foreign key.
    params:          JSON encoded dict of the parameters for the job. This
                      can be fetched out of the database by the worker processes
                      based on the jobID.
    minimumWorkers:  minimum number of workers design at a time.
    maximumWorkers:  maximum number of workers desired at a time.
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
    alreadyRunning:  Used for unit test purposes only. This inserts the job
                      in the running state. It is used when running a worker
                      in standalone mode without hadoop- it gives it a job
                      record to work with.

    retval:           jobID of the inserted jobs row, or of an existing jobs row
                       with matching client/jobHash key
    """

    assert len(client) <= self.CLIENT_MAX_LEN, "client too long:" + repr(client)
    assert cmdLine, "Unexpected empty or None command-line: " + repr(cmdLine)
    assert len(jobHash) == self.HASH_MAX_LEN, "wrong hash len=%d" % len(jobHash)

    # Initial status
    if alreadyRunning:
      # STATUS_TESTMODE, so that scheduler won't pick it up (for in-proc tests)
      initStatus = self.STATUS_TESTMODE
    else:
      initStatus = self.STATUS_NOTSTARTED

    # Create a new job entry
    query = 'INSERT IGNORE INTO %s (status, client, client_info, client_key,' \
            'cmd_line, params, job_hash, _eng_last_update_time, ' \
            'minimum_workers, maximum_workers, priority, _eng_job_type) ' \
            ' VALUES (%%s, %%s, %%s, %%s, %%s, %%s, %%s, ' \
            '         UTC_TIMESTAMP(), %%s, %%s, %%s, %%s) ' \
            % (self.jobsTableName,)
    sqlParams = (initStatus, client, clientInfo, clientKey, cmdLine, params,
                 jobHash, minimumWorkers, maximumWorkers, priority, jobType)
    numRowsInserted = conn.cursor.execute(query, sqlParams)

    jobID = 0

    if numRowsInserted == 1:
      # Get the chosen job id
      # NOTE: LAST_INSERT_ID() returns 0 after intermittent connection failure
      conn.cursor.execute('SELECT LAST_INSERT_ID()')
      jobID = conn.cursor.fetchall()[0][0]
      if jobID == 0:
        self._logger.warn(
          '_insertOrGetUniqueJobNoRetries: SELECT LAST_INSERT_ID() returned 0; '
          'likely due to reconnection in SteadyDB following INSERT. '
          'jobType=%r; client=%r; clientInfo=%r; clientKey=%s; jobHash=%r; '
          'cmdLine=%r',
          jobType, client, _abbreviate(clientInfo, 32), clientKey, jobHash,
          cmdLine)
    else:
      # Assumption: nothing was inserted because this is a retry and the row
      # with this client/hash already exists from our prior
      # partially-successful attempt; or row with matching client/jobHash was
      # inserted already by some process on some machine.
      assert numRowsInserted == 0, repr(numRowsInserted)

    if jobID == 0:
      # Recover from intermittent failure in a partially-successful attempt;
      # or row with matching client/jobHash was already in table
      row = self._getOneMatchingRowNoRetries(
        self._jobs, conn, dict(client=client, job_hash=jobHash), ['job_id'])
      assert row is not None
      assert len(row) == 1, 'Unexpected num fields: ' + repr(len(row))
      jobID = row[0]

    # ---------------------------------------------------------------------
    # If asked to enter the job in the running state, set the connection id
    #  and start time as well
    if alreadyRunning:
      query = 'UPDATE %s SET _eng_cjm_conn_id=%%s, ' \
              '              start_time=UTC_TIMESTAMP(), ' \
              '              _eng_last_update_time=UTC_TIMESTAMP() ' \
              '          WHERE job_id=%%s' \
              % (self.jobsTableName,)
      conn.cursor.execute(query, (self._connectionID, jobID))

    return jobID