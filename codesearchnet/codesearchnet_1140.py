def getJobStatus(self, workers):
    """
    Parameters:
    ----------------------------------------------------------------------
    workers:  If this job was launched outside of the nupic job engine, then this
               is an array of subprocess Popen instances, one for each worker
    retval:         _NupicJob.JobStatus instance

    """
    jobInfo = self.JobStatus(self.__nupicJobID, workers)
    return jobInfo