def jobInsert(self, client, cmdLine, clientInfo='', clientKey='', params='',
                alreadyRunning=False, minimumWorkers=0, maximumWorkers=0,
                jobType='', priority=DEFAULT_JOB_PRIORITY):
    """ Add an entry to the jobs table for a new job request. This is called by
    clients that wish to startup a new job, like a Hypersearch, stream job, or
    specific model evaluation from the engine.

    This puts a new entry into the jobs table. The CJM is always periodically
    sweeping the jobs table and when it finds a new job, will proceed to start it
    up on Hadoop.

    Parameters:
    ----------------------------------------------------------------
    client:          Name of the client submitting the job
    cmdLine:         Command line to use to launch each worker process; must be
                      a non-empty string
    clientInfo:      JSON encoded dict of client specific information.
    clientKey:       Foreign key.
    params:          JSON encoded dict of the parameters for the job. This
                      can be fetched out of the database by the worker processes
                      based on the jobID.
    alreadyRunning:  Used for unit test purposes only. This inserts the job
                      in the running state. It is used when running a worker
                      in standalone mode without hadoop - it gives it a job
                      record to work with.
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

    retval:          jobID - unique ID assigned to this job
    """

    jobHash = self._normalizeHash(uuid.uuid1().bytes)

    @g_retrySQL
    def insertWithRetries():
      with ConnectionFactory.get() as conn:
        return self._insertOrGetUniqueJobNoRetries(
          conn, client=client, cmdLine=cmdLine, jobHash=jobHash,
          clientInfo=clientInfo, clientKey=clientKey, params=params,
          minimumWorkers=minimumWorkers, maximumWorkers=maximumWorkers,
          jobType=jobType, priority=priority, alreadyRunning=alreadyRunning)

    try:
      jobID = insertWithRetries()
    except:
      self._logger.exception(
        'jobInsert FAILED: jobType=%r; client=%r; clientInfo=%r; clientKey=%r;'
        'jobHash=%r; cmdLine=%r',
        jobType, client, _abbreviate(clientInfo, 48), clientKey, jobHash,
        cmdLine)
      raise
    else:
      self._logger.info(
        'jobInsert: returning jobID=%s. jobType=%r; client=%r; clientInfo=%r; '
        'clientKey=%r; jobHash=%r; cmdLine=%r',
        jobID, jobType, client, _abbreviate(clientInfo, 48), clientKey,
        jobHash, cmdLine)

    return jobID