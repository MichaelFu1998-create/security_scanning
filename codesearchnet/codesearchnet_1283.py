def jobGetDemand(self,):
    """ Look through the jobs table and get the demand - minimum and maximum
    number of workers requested, if new workers are to be allocated, if there
    are any untended dead workers, for all running jobs.

    Parameters:
    ----------------------------------------------------------------
    retval:      list of ClientJobsDAO._jobs.jobDemandNamedTuple nametuples
                  containing the demand - min and max workers,
                  allocate_new_workers, untended_dead_workers, num_failed_workers
                  for each running (STATUS_RUNNING) job. Empty list when there
                  isn't any demand.

    """
    rows = self._getMatchingRowsWithRetries(
      self._jobs, dict(status=self.STATUS_RUNNING),
      [self._jobs.pubToDBNameDict[f]
       for f in self._jobs.jobDemandNamedTuple._fields])

    return [self._jobs.jobDemandNamedTuple._make(r) for r in rows]