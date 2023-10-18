def jobStartNext(self):
    """ For use only by Nupic Scheduler (also known as ClientJobManager) Look
    through the jobs table and see if any new job requests have been
    queued up. If so, pick one and mark it as starting up and create the
    model table to hold the results

    Parameters:
    ----------------------------------------------------------------
    retval:    jobID of the job we are starting up, if found; None if not found
    """

    # NOTE: cursor.execute('SELECT @update_id') trick is unreliable: if a
    #  connection loss occurs during cursor.execute, then the server-cached
    #  information is lost, and we cannot get the updated job ID; so, we use
    #  this select instead
    row = self._getOneMatchingRowWithRetries(
      self._jobs, dict(status=self.STATUS_NOTSTARTED), ['job_id'])
    if row is None:
      return None

    (jobID,) = row

    self._startJobWithRetries(jobID)

    return jobID