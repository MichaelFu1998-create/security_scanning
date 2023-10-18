def __setAsOrphaned(self):
    """
    Sets the current model as orphaned. This is called when the scheduler is
    about to kill the process to reallocate the worker to a different process.
    """
    cmplReason = ClientJobsDAO.CMPL_REASON_ORPHAN
    cmplMessage = "Killed by Scheduler"
    self._jobsDAO.modelSetCompleted(self._modelID, cmplReason, cmplMessage)