def jobInfo(self, jobID):
    """ Get all info about a job

    Parameters:
    ----------------------------------------------------------------
    job:    jobID of the job to query
    retval:  namedtuple containing the job info.

    """
    row = self._getOneMatchingRowWithRetries(
      self._jobs, dict(job_id=jobID),
      [self._jobs.pubToDBNameDict[n]
       for n in self._jobs.jobInfoNamedTuple._fields])

    if row is None:
      raise RuntimeError("jobID=%s not found within the jobs table" % (jobID))

    # Create a namedtuple with the names to values
    return self._jobs.jobInfoNamedTuple._make(row)