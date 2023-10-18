def __runTaskMainLoop(self, numIters, learningOffAt=None):
    """ Main loop of the OPF Model Runner.

    Parameters:
    -----------------------------------------------------------------------

    recordIterator:    Iterator for counting number of records (see _runTask)
    learningOffAt:     If not None, learning is turned off when we reach this
                        iteration number

    """

    ## Reset sequence states in the model, so it starts looking for a new
    ## sequence
    self._model.resetSequenceStates()

    self._currentRecordIndex = -1
    while True:

      # If killed by a terminator, stop running
      if self._isKilled:
        break

      # If job stops or hypersearch ends, stop running
      if self._isCanceled:
        break

      # If the process is about to be killed, set as orphaned
      if self._isInterrupted.isSet():
        self.__setAsOrphaned()
        break

      # If model is mature, stop running ONLY IF  we are not the best model
      # for the job. Otherwise, keep running so we can keep returning
      # predictions to the user
      if self._isMature:
        if not self._isBestModel:
          self._cmpReason = self._jobsDAO.CMPL_REASON_STOPPED
          break
        else:
          self._cmpReason = self._jobsDAO.CMPL_REASON_EOF

      # Turn off learning?
        if learningOffAt is not None \
                  and self._currentRecordIndex == learningOffAt:
          self._model.disableLearning()

      # Read input record. Note that any failure here is a critical JOB failure
      #  and results in the job being immediately canceled and marked as
      #  failed. The runModelXXX code in hypesearch.utils, if it sees an
      #  exception of type utils.JobFailException, will cancel the job and
      #  copy the error message into the job record.
      try:
        inputRecord = self._inputSource.getNextRecordDict()
        if self._currentRecordIndex < 0:
          self._inputSource.setTimeout(10)
      except Exception, e:
        raise utils.JobFailException(ErrorCodes.streamReading, str(e.args),
                                     traceback.format_exc())

      if inputRecord is None:
        # EOF
        self._cmpReason = self._jobsDAO.CMPL_REASON_EOF
        break

      if inputRecord:
        # Process input record
        self._currentRecordIndex += 1

        result = self._model.run(inputRecord=inputRecord)

        # Compute metrics.
        result.metrics = self.__metricMgr.update(result)
        # If there are None, use defaults. see MetricsManager.getMetrics()
        # TODO remove this when JAVA API server is gone
        if not result.metrics:
          result.metrics = self.__metricMgr.getMetrics()


        # Write the result to the output cache. Don't write encodings, if they
        # were computed
        if InferenceElement.encodings in result.inferences:
          result.inferences.pop(InferenceElement.encodings)
        result.sensorInput.dataEncodings = None
        self._writePrediction(result)

        # Run periodic activities
        self._periodic.tick()

        if numIters >= 0 and self._currentRecordIndex >= numIters-1:
          break

      else:
        # Input source returned an empty record.
        #
        # NOTE: This is okay with Stream-based Source (when it times out
        # waiting for next record), but not okay with FileSource, which should
        # always return either with a valid record or None for EOF.
        raise ValueError("Got an empty record from FileSource: %r" %
                         inputRecord)