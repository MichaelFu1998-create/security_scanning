def __checkCancelation(self):
    """ Check if the cancelation flag has been set for this model
    in the Model DB"""

    # Update a hadoop job counter at least once every 600 seconds so it doesn't
    #  think our map task is dead
    print >>sys.stderr, "reporter:counter:HypersearchWorker,numRecords,50"

    # See if the job got cancelled
    jobCancel = self._jobsDAO.jobGetFields(self._jobID, ['cancel'])[0]
    if jobCancel:
      self._cmpReason = ClientJobsDAO.CMPL_REASON_KILLED
      self._isCanceled = True
      self._logger.info("Model %s canceled because Job %s was stopped.",
                        self._modelID, self._jobID)
    else:
      stopReason = self._jobsDAO.modelsGetFields(self._modelID, ['engStop'])[0]

      if stopReason is None:
        pass

      elif stopReason == ClientJobsDAO.STOP_REASON_KILLED:
        self._cmpReason = ClientJobsDAO.CMPL_REASON_KILLED
        self._isKilled = True
        self._logger.info("Model %s canceled because it was killed by hypersearch",
                          self._modelID)

      elif stopReason == ClientJobsDAO.STOP_REASON_STOPPED:
        self._cmpReason = ClientJobsDAO.CMPL_REASON_STOPPED
        self._isCanceled = True
        self._logger.info("Model %s stopped because hypersearch ended", self._modelID)
      else:
        raise RuntimeError ("Unexpected stop reason encountered: %s" % (stopReason))