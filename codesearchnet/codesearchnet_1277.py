def jobResume(self, jobID, alreadyRunning=False):
    """ Resumes processing of an existing job that is presently in the
    STATUS_COMPLETED state.

    NOTE: this is primarily for resuming suspended Production Jobs; DO NOT use
    it on Hypersearch jobs.

    NOTE: The job MUST be in the STATUS_COMPLETED state at the time of this
    call, otherwise an exception will be raised.

    This prepares an existing job entry to resume processing. The CJM is always
    periodically sweeping the jobs table and when it finds a job that is ready
    to run, will proceed to start it up on Hadoop.

    Parameters:
    ----------------------------------------------------------------
    job:            jobID of the job to resume
    alreadyRunning: Used for unit test purposes only. This inserts the job
                     in the running state. It is used when running a worker
                     in standalone mode without hadoop.

    raises:         Throws a RuntimeError if no rows are affected. This could
                    either be because:
                      1) Because there was not matching jobID
                      2) or if the status of the job was not STATUS_COMPLETED.

    retval:            nothing
    """

    row = self.jobGetFields(jobID, ['status'])
    (jobStatus,) = row
    if jobStatus != self.STATUS_COMPLETED:
      raise RuntimeError(("Failed to resume job: job was not suspended; "
                          "jobID=%s; job status=%r") % (jobID, jobStatus))

    # NOTE: on MySQL failures, we need to retry ConnectionFactory.get() as well
    #  in order to recover from lost connections
    @g_retrySQL
    def resumeWithRetries():
      with ConnectionFactory.get() as conn:
        self._resumeJobNoRetries(conn, jobID, alreadyRunning)

    resumeWithRetries()
    return