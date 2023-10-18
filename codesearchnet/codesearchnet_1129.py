def monitorSearchJob(self):
    """
    Parameters:
    ----------------------------------------------------------------------
    retval:         nothing
    """
    assert self.__searchJob is not None

    jobID = self.__searchJob.getJobID()

    startTime = time.time()
    lastUpdateTime = datetime.now()

    # Monitor HyperSearch and report progress

    # NOTE: may be -1 if it can't be determined
    expectedNumModels = self.__searchJob.getExpectedNumModels(
                                searchMethod = self._options["searchMethod"])

    lastNumFinished = 0
    finishedModelIDs = set()

    finishedModelStats = _ModelStats()

    # Keep track of the worker state, results, and milestones from the job
    # record
    lastWorkerState = None
    lastJobResults = None
    lastModelMilestones = None
    lastEngStatus = None

    hyperSearchFinished = False
    while not hyperSearchFinished:
      jobInfo = self.__searchJob.getJobStatus(self._workers)

      # Check for job completion BEFORE processing models; NOTE: this permits us
      # to process any models that we may not have accounted for in the
      # previous iteration.
      hyperSearchFinished = jobInfo.isFinished()

      # Look for newly completed models, and process them
      modelIDs = self.__searchJob.queryModelIDs()
      _emit(Verbosity.DEBUG,
            "Current number of models is %d (%d of them completed)" % (
              len(modelIDs), len(finishedModelIDs)))

      if len(modelIDs) > 0:
        # Build a list of modelIDs to check for completion
        checkModelIDs = []
        for modelID in modelIDs:
          if modelID not in finishedModelIDs:
            checkModelIDs.append(modelID)

        del modelIDs

        # Process newly completed models
        if checkModelIDs:
          _emit(Verbosity.DEBUG,
                "Checking %d models..." % (len(checkModelIDs)))
          errorCompletionMsg = None
          for (i, modelInfo) in enumerate(_iterModels(checkModelIDs)):
            _emit(Verbosity.DEBUG,
                  "[%s] Checking completion: %s" % (i, modelInfo))
            if modelInfo.isFinished():
              finishedModelIDs.add(modelInfo.getModelID())

              finishedModelStats.update(modelInfo)

              if (modelInfo.getCompletionReason().isError() and
                  not errorCompletionMsg):
                errorCompletionMsg = modelInfo.getCompletionMsg()

              # Update the set of all encountered metrics keys (we will use
              # these to print column names in reports.csv)
              metrics = modelInfo.getReportMetrics()
              self.__foundMetrcsKeySet.update(metrics.keys())

        numFinished = len(finishedModelIDs)

        # Print current completion stats
        if numFinished != lastNumFinished:
          lastNumFinished = numFinished

          if expectedNumModels is None:
            expModelsStr = ""
          else:
            expModelsStr = "of %s" % (expectedNumModels)

          stats = finishedModelStats
          print ("<jobID: %s> %s %s models finished [success: %s; %s: %s; %s: "
                 "%s; %s: %s; %s: %s; %s: %s; %s: %s]" % (
                     jobID,
                     numFinished,
                     expModelsStr,
                     #stats.numCompletedSuccess,
                     (stats.numCompletedEOF+stats.numCompletedStopped),
                     "EOF" if stats.numCompletedEOF else "eof",
                     stats.numCompletedEOF,
                     "STOPPED" if stats.numCompletedStopped else "stopped",
                     stats.numCompletedStopped,
                     "KILLED" if stats.numCompletedKilled else "killed",
                     stats.numCompletedKilled,
                     "ERROR" if stats.numCompletedError else "error",
                     stats.numCompletedError,
                     "ORPHANED" if stats.numCompletedError else "orphaned",
                     stats.numCompletedOrphaned,
                     "UNKNOWN" if stats.numCompletedOther else "unknown",
                     stats.numCompletedOther))

          # Print the first error message from the latest batch of completed
          # models
          if errorCompletionMsg:
            print "ERROR MESSAGE: %s" % errorCompletionMsg

        # Print the new worker state, if it changed
        workerState = jobInfo.getWorkerState()
        if workerState != lastWorkerState:
          print "##>> UPDATED WORKER STATE: \n%s" % (pprint.pformat(workerState,
                                                           indent=4))
          lastWorkerState = workerState

        # Print the new job results, if it changed
        jobResults = jobInfo.getResults()
        if jobResults != lastJobResults:
          print "####>> UPDATED JOB RESULTS: \n%s (elapsed time: %g secs)" \
              % (pprint.pformat(jobResults, indent=4), time.time()-startTime)
          lastJobResults = jobResults

        # Print the new model milestones if they changed
        modelMilestones = jobInfo.getModelMilestones()
        if modelMilestones != lastModelMilestones:
          print "##>> UPDATED MODEL MILESTONES: \n%s" % (
              pprint.pformat(modelMilestones, indent=4))
          lastModelMilestones = modelMilestones

        # Print the new engine status if it changed
        engStatus = jobInfo.getEngStatus()
        if engStatus != lastEngStatus:
          print "##>> UPDATED STATUS: \n%s" % (engStatus)
          lastEngStatus = engStatus

      # Sleep before next check
      if not hyperSearchFinished:
        if self._options["timeout"] != None:
          if ((datetime.now() - lastUpdateTime) >
              timedelta(minutes=self._options["timeout"])):
            print "Timeout reached, exiting"
            self.__cjDAO.jobCancel(jobID)
            sys.exit(1)
        time.sleep(1)

    # Tabulate results
    modelIDs = self.__searchJob.queryModelIDs()
    print "Evaluated %s models" % len(modelIDs)
    print "HyperSearch finished!"

    jobInfo = self.__searchJob.getJobStatus(self._workers)
    print "Worker completion message: %s" % (jobInfo.getWorkerCompletionMsg())