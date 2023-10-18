def run(self):
    """ Runs the given OPF task against the given Model instance """

    self._logger.debug("Starting Dummy Model: modelID=%s;" % (self._modelID))

    # =========================================================================
    # Initialize periodic activities (e.g., for model result updates)
    # =========================================================================
    periodic = self._initPeriodicActivities()

    self._optimizedMetricLabel = self._optimizeKeyPattern
    self._reportMetricLabels = [self._optimizeKeyPattern]

    # =========================================================================
    # Create our top-level loop-control iterator
    # =========================================================================
    if self._iterations >= 0:
      iterTracker = iter(xrange(self._iterations))
    else:
      iterTracker = iter(itertools.count())

    # =========================================================================
    # This gets set in the unit tests. It tells the worker to sys exit
    #  the first N models. This is how we generate orphaned models
    doSysExit = False
    if self._sysExitModelRange is not None:
      modelAndCounters = self._jobsDAO.modelsGetUpdateCounters(self._jobID)
      modelIDs = [x[0] for x in modelAndCounters]
      modelIDs.sort()
      (beg,end) = self._sysExitModelRange
      if self._modelID in modelIDs[int(beg):int(end)]:
        doSysExit = True

    if self._delayModelRange is not None:
      modelAndCounters = self._jobsDAO.modelsGetUpdateCounters(self._jobID)
      modelIDs = [x[0] for x in modelAndCounters]
      modelIDs.sort()
      (beg,end) = self._delayModelRange
      if self._modelID in modelIDs[int(beg):int(end)]:
        time.sleep(10)

      # DEBUG!!!! infinite wait if we have 50 models
      #if len(modelIDs) >= 50:
      #  jobCancel = self._jobsDAO.jobGetFields(self._jobID, ['cancel'])[0]
      #  while not jobCancel:
      #    time.sleep(1)
      #    jobCancel = self._jobsDAO.jobGetFields(self._jobID, ['cancel'])[0]

    if self._errModelRange is not None:
      modelAndCounters = self._jobsDAO.modelsGetUpdateCounters(self._jobID)
      modelIDs = [x[0] for x in modelAndCounters]
      modelIDs.sort()
      (beg,end) = self._errModelRange
      if self._modelID in modelIDs[int(beg):int(end)]:
        raise RuntimeError("Exiting with error due to errModelRange parameter")

    # =========================================================================
    # Delay, if necessary
    if self._delay is not None:
      time.sleep(self._delay)

    # =========================================================================
    # Run it!
    # =========================================================================
    self._currentRecordIndex = 0
    while True:

      # =========================================================================
      # Check if the model should be stopped
      # =========================================================================

      # If killed by a terminator, stop running
      if self._isKilled:
        break

      # If job stops or hypersearch ends, stop running
      if self._isCanceled:
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

      # =========================================================================
      # Get the the next record, and "write it"
      # =========================================================================
      try:
        self._currentRecordIndex = next(iterTracker)
      except StopIteration:
        break

      # "Write" a dummy output value. This is used to test that the batched
      # writing works properly

      self._writePrediction(ModelResult(None, None, None, None))

      periodic.tick()

      # =========================================================================
      # Compute wait times. See if model should exit
      # =========================================================================

      if self.__shouldSysExit(self._currentRecordIndex):
        sys.exit(1)

      # Simulate computation time
      if self._busyWaitTime is not None:
        time.sleep(self._busyWaitTime)
        self.__computeWaitTime()

      # Asked to abort after so many iterations?
      if doSysExit:
        sys.exit(1)

      # Asked to raise a jobFailException?
      if self._jobFailErr:
        raise utils.JobFailException("E10000",
                                      "dummyModel's jobFailErr was True.")

    # =========================================================================
    # Handle final operations
    # =========================================================================
    if self._doFinalize:
      if not self._makeCheckpoint:
        self._model = None

      # Delay finalization operation
      if self._finalDelay is not None:
        time.sleep(self._finalDelay)

      self._finalize()

    self._logger.info("Finished: modelID=%r "% (self._modelID))

    return (self._cmpReason, None)