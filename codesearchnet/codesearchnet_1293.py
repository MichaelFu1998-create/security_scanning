def jobCancel(self, jobID):
    """ Cancel the given job. This will update the cancel field in the
    jobs table and will result in the job being cancelled.

    Parameters:
    ----------------------------------------------------------------
    jobID:                 jobID of the job to mark as completed

    to False for hypersearch workers
    """
    self._logger.info('Canceling jobID=%s', jobID)
    # NOTE: jobSetFields does retries on transient mysql failures
    self.jobSetFields(jobID, {"cancel" : True}, useConnectionID=False)