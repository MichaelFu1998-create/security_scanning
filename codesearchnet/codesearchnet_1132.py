def generateReport(cls,
                     options,
                     replaceReport,
                     hyperSearchJob,
                     metricsKeys):
    """Prints all available results in the given HyperSearch job and emits
    model information to the permutations report csv.

    The job may be completed or still in progress.

    Parameters:
    ----------------------------------------------------------------------
    options:        NupicRunPermutations options dict
    replaceReport:  True to replace existing report csv, if any; False to
                    append to existing report csv, if any
    hyperSearchJob: _HyperSearchJob instance; if None, will get it from saved
                    jobID, if any
    metricsKeys:    sequence of report metrics key names to include in report;
                    if None, will pre-scan all modelInfos to generate a complete
                    list of metrics key names.
    retval:         model parameters
    """
    # Load _HyperSearchJob instance from storage, if not provided
    if hyperSearchJob is None:
      hyperSearchJob = cls.loadSavedHyperSearchJob(
          permWorkDir=options["permWorkDir"],
          outputLabel=options["outputLabel"])

    modelIDs = hyperSearchJob.queryModelIDs()
    bestModel = None

    # If metricsKeys was not provided, pre-scan modelInfos to create the list;
    # this is needed by _ReportCSVWriter
    # Also scan the parameters to generate a list of encoders and search
    # parameters
    metricstmp = set()
    searchVar = set()
    for modelInfo in _iterModels(modelIDs):
      if modelInfo.isFinished():
        vars = modelInfo.getParamLabels().keys()
        searchVar.update(vars)
        metrics = modelInfo.getReportMetrics()
        metricstmp.update(metrics.keys())
    if metricsKeys is None:
      metricsKeys = metricstmp
    # Create a csv report writer
    reportWriter = _ReportCSVWriter(hyperSearchJob=hyperSearchJob,
                                    metricsKeys=metricsKeys,
                                    searchVar=searchVar,
                                    outputDirAbsPath=options["permWorkDir"],
                                    outputLabel=options["outputLabel"],
                                    replaceReport=replaceReport)

    # Tallies of experiment dispositions
    modelStats = _ModelStats()
    #numCompletedOther = long(0)

    print "\nResults from all experiments:"
    print "----------------------------------------------------------------"

    # Get common optimization metric info from permutations script
    searchParams = hyperSearchJob.getParams()

    (optimizationMetricKey, maximizeMetric) = (
      _PermutationUtils.getOptimizationMetricInfo(searchParams))

    # Print metrics, while looking for the best model
    formatStr = None
    # NOTE: we may find additional metrics if HyperSearch is still running
    foundMetricsKeySet = set(metricsKeys)
    sortedMetricsKeys = []

    # pull out best Model from jobs table
    jobInfo = _clientJobsDB().jobInfo(hyperSearchJob.getJobID())

    # Try to return a decent error message if the job was cancelled for some
    # reason.
    if jobInfo.cancel == 1:
      raise Exception(jobInfo.workerCompletionMsg)

    try:
      results = json.loads(jobInfo.results)
    except Exception, e:
      print "json.loads(jobInfo.results) raised an exception.  " \
            "Here is some info to help with debugging:"
      print "jobInfo: ", jobInfo
      print "jobInfo.results: ", jobInfo.results
      print "EXCEPTION: ", e
      raise

    bestModelNum = results["bestModel"]
    bestModelIterIndex = None

    # performance metrics for the entire job
    totalWallTime = 0
    totalRecords = 0

    # At the end, we will sort the models by their score on the optimization
    # metric
    scoreModelIDDescList = []
    for (i, modelInfo) in enumerate(_iterModels(modelIDs)):

      # Output model info to report csv
      reportWriter.emit(modelInfo)

      # Update job metrics
      totalRecords+=modelInfo.getNumRecords()
      format = "%Y-%m-%d %H:%M:%S"
      startTime = modelInfo.getStartTime()
      if modelInfo.isFinished():
        endTime = modelInfo.getEndTime()
        st = datetime.strptime(startTime, format)
        et = datetime.strptime(endTime, format)
        totalWallTime+=(et-st).seconds

      # Tabulate experiment dispositions
      modelStats.update(modelInfo)

      # For convenience
      expDesc = modelInfo.getModelDescription()
      reportMetrics = modelInfo.getReportMetrics()
      optimizationMetrics = modelInfo.getOptimizationMetrics()
      if modelInfo.getModelID() == bestModelNum:
        bestModel = modelInfo
        bestModelIterIndex=i
        bestMetric = optimizationMetrics.values()[0]

      # Keep track of the best-performing model
      if optimizationMetrics:
        assert len(optimizationMetrics) == 1, (
            "expected 1 opt key, but got %d (%s) in %s" % (
                len(optimizationMetrics), optimizationMetrics, modelInfo))

      # Append to our list of modelIDs and scores
      if modelInfo.getCompletionReason().isEOF():
        scoreModelIDDescList.append((optimizationMetrics.values()[0],
                                    modelInfo.getModelID(),
                                    modelInfo.getGeneratedDescriptionFile(),
                                    modelInfo.getParamLabels()))

      print "[%d] Experiment %s\n(%s):" % (i, modelInfo, expDesc)
      if (modelInfo.isFinished() and
          not (modelInfo.getCompletionReason().isStopped or
               modelInfo.getCompletionReason().isEOF())):
        print ">> COMPLETION MESSAGE: %s" % modelInfo.getCompletionMsg()

      if reportMetrics:
        # Update our metrics key set and format string
        foundMetricsKeySet.update(reportMetrics.iterkeys())
        if len(sortedMetricsKeys) != len(foundMetricsKeySet):
          sortedMetricsKeys = sorted(foundMetricsKeySet)

          maxKeyLen = max([len(k) for k in sortedMetricsKeys])
          formatStr = "  %%-%ds" % (maxKeyLen+2)

        # Print metrics
        for key in sortedMetricsKeys:
          if key in reportMetrics:
            if key == optimizationMetricKey:
              m = "%r (*)" % reportMetrics[key]
            else:
              m = "%r" % reportMetrics[key]
            print formatStr % (key+":"), m
        print

    # Summarize results
    print "--------------------------------------------------------------"
    if len(modelIDs) > 0:
      print "%d experiments total (%s).\n" % (
          len(modelIDs),
          ("all completed successfully"
           if (modelStats.numCompletedKilled + modelStats.numCompletedEOF) ==
               len(modelIDs)
           else "WARNING: %d models have not completed or there were errors" % (
               len(modelIDs) - (
                   modelStats.numCompletedKilled + modelStats.numCompletedEOF +
                   modelStats.numCompletedStopped))))

      if modelStats.numStatusOther > 0:
        print "ERROR: models with unexpected status: %d" % (
            modelStats.numStatusOther)

      print "WaitingToStart: %d" % modelStats.numStatusWaitingToStart
      print "Running: %d" % modelStats.numStatusRunning
      print "Completed: %d" % modelStats.numStatusCompleted
      if modelStats.numCompletedOther > 0:
        print "    ERROR: models with unexpected completion reason: %d" % (
            modelStats.numCompletedOther)
      print "    ran to EOF: %d" % modelStats.numCompletedEOF
      print "    ran to stop signal: %d" % modelStats.numCompletedStopped
      print "    were orphaned: %d" % modelStats.numCompletedOrphaned
      print "    killed off: %d" % modelStats.numCompletedKilled
      print "    failed: %d" % modelStats.numCompletedError

      assert modelStats.numStatusOther == 0, "numStatusOther=%s" % (
          modelStats.numStatusOther)
      assert modelStats.numCompletedOther == 0, "numCompletedOther=%s" % (
          modelStats.numCompletedOther)

    else:
      print "0 experiments total."

    # Print out the field contributions
    print
    global gCurrentSearch
    jobStatus = hyperSearchJob.getJobStatus(gCurrentSearch._workers)
    jobResults = jobStatus.getResults()
    if "fieldContributions" in jobResults:
      print "Field Contributions:"
      pprint.pprint(jobResults["fieldContributions"], indent=4)
    else:
      print "Field contributions info not available"

    # Did we have an optimize key?
    if bestModel is not None:
      maxKeyLen = max([len(k) for k in sortedMetricsKeys])
      maxKeyLen = max(maxKeyLen, len(optimizationMetricKey))
      formatStr = "  %%-%ds" % (maxKeyLen+2)
      bestMetricValue = bestModel.getOptimizationMetrics().values()[0]
      optimizationMetricName = bestModel.getOptimizationMetrics().keys()[0]
      print
      print "Best results on the optimization metric %s (maximize=%s):" % (
          optimizationMetricName, maximizeMetric)
      print "[%d] Experiment %s (%s):" % (
          bestModelIterIndex, bestModel, bestModel.getModelDescription())
      print formatStr % (optimizationMetricName+":"), bestMetricValue
      print
      print "Total number of Records processed: %d"  % totalRecords
      print
      print "Total wall time for all models: %d" % totalWallTime

      hsJobParams = hyperSearchJob.getParams()

    # Were we asked to write out the top N model description files?
    if options["genTopNDescriptions"] > 0:
      print "\nGenerating description files for top %d models..." % (
              options["genTopNDescriptions"])
      scoreModelIDDescList.sort()
      scoreModelIDDescList = scoreModelIDDescList[
          0:options["genTopNDescriptions"]]

      i = -1
      for (score, modelID, description, paramLabels) in scoreModelIDDescList:
        i += 1
        outDir = os.path.join(options["permWorkDir"], "model_%d" % (i))
        print "Generating description file for model %s at %s" % \
          (modelID, outDir)
        if not os.path.exists(outDir):
          os.makedirs(outDir)

        # Fix up the location to the base description file.
        # importBaseDescription() chooses the file relative to the calling file.
        # The calling file is in outDir.
        # The base description is in the user-specified "outDir"
        base_description_path = os.path.join(options["outDir"],
          "description.py")
        base_description_relpath = os.path.relpath(base_description_path,
          start=outDir)
        description = description.replace(
              "importBaseDescription('base.py', config)",
              "importBaseDescription('%s', config)" % base_description_relpath)
        fd = open(os.path.join(outDir, "description.py"), "wb")
        fd.write(description)
        fd.close()

        # Generate a csv file with the parameter settings in it
        fd = open(os.path.join(outDir, "params.csv"), "wb")
        writer = csv.writer(fd)
        colNames = paramLabels.keys()
        colNames.sort()
        writer.writerow(colNames)
        row = [paramLabels[x] for x in colNames]
        writer.writerow(row)
        fd.close()

        print "Generating model params file..."
        # Generate a model params file alongside the description.py
        mod = imp.load_source("description", os.path.join(outDir,
                                                          "description.py"))
        model_description = mod.descriptionInterface.getModelDescription()
        fd = open(os.path.join(outDir, "model_params.py"), "wb")
        fd.write("%s\nMODEL_PARAMS = %s" % (getCopyrightHead(),
                                            pprint.pformat(model_description)))
        fd.close()

      print

    reportWriter.finalize()
    return model_description