def __startSearch(self):
    """Starts HyperSearch as a worker or runs it inline for the "dryRun" action

    Parameters:
    ----------------------------------------------------------------------
    retval:         the new _HyperSearchJob instance representing the
                    HyperSearch job
    """
    # This search uses a pre-existing permutations script
    params = _ClientJobUtils.makeSearchJobParamsDict(options=self._options,
                                                     forRunning=True)

    if self._options["action"] == "dryRun":
      args = [sys.argv[0], "--params=%s" % (json.dumps(params))]

      print
      print "=================================================================="
      print "RUNNING PERMUTATIONS INLINE as \"DRY RUN\"..."
      print "=================================================================="
      jobID = hypersearch_worker.main(args)

    else:
      cmdLine = _setUpExports(self._options["exports"])
      # Begin the new search. The {JOBID} string is replaced by the actual
      # jobID returned from jobInsert.
      cmdLine += "$HYPERSEARCH"
      maxWorkers = self._options["maxWorkers"]

      jobID = self.__cjDAO.jobInsert(
        client="GRP",
        cmdLine=cmdLine,
        params=json.dumps(params),
        minimumWorkers=1,
        maximumWorkers=maxWorkers,
        jobType=self.__cjDAO.JOB_TYPE_HS)

      cmdLine = "python -m nupic.swarming.hypersearch_worker" \
                 " --jobID=%d" % (jobID)
      self._launchWorkers(cmdLine, maxWorkers)

    searchJob = _HyperSearchJob(jobID)

    # Save search ID to file (this is used for report generation)
    self.__saveHyperSearchJobID(
      permWorkDir=self._options["permWorkDir"],
      outputLabel=self._options["outputLabel"],
      hyperSearchJob=searchJob)

    if self._options["action"] == "dryRun":
      print "Successfully executed \"dry-run\" hypersearch, jobID=%d" % (jobID)
    else:
      print "Successfully submitted new HyperSearch job, jobID=%d" % (jobID)
      _emit(Verbosity.DEBUG,
            "Each worker executing the command line: %s" % (cmdLine,))

    return searchJob