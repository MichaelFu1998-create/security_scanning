def run(self):
    """ Run this worker.

    Parameters:
    ----------------------------------------------------------------------
    retval:     jobID of the job we ran. This is used by unit test code
                  when calling this working using the --params command
                  line option (which tells this worker to insert the job
                  itself).
    """
    # Easier access to options
    options = self._options

    # ---------------------------------------------------------------------
    # Connect to the jobs database
    self.logger.info("Connecting to the jobs database")
    cjDAO = ClientJobsDAO.get()

    # Get our worker ID
    self._workerID = cjDAO.getConnectionID()

    if options.clearModels:
      cjDAO.modelsClearAll()

    # -------------------------------------------------------------------------
    # if params were specified on the command line, insert a new job using
    #  them.
    if options.params is not None:
      options.jobID = cjDAO.jobInsert(client='hwTest', cmdLine="echo 'test mode'",
                  params=options.params, alreadyRunning=True,
                  minimumWorkers=1, maximumWorkers=1,
                  jobType = cjDAO.JOB_TYPE_HS)
    if options.workerID is not None:
      wID = options.workerID
    else:
      wID = self._workerID

    buildID = Configuration.get('nupic.software.buildNumber', 'N/A')
    logPrefix = '<BUILDID=%s, WORKER=HW, WRKID=%s, JOBID=%s> ' % \
                (buildID, wID, options.jobID)
    ExtendedLogger.setLogPrefix(logPrefix)

    # ---------------------------------------------------------------------
    # Get the search parameters
    # If asked to reset the job status, do that now
    if options.resetJobStatus:
      cjDAO.jobSetFields(options.jobID,
           fields={'workerCompletionReason': ClientJobsDAO.CMPL_REASON_SUCCESS,
                   'cancel': False,
                   #'engWorkerState': None
                   },
           useConnectionID=False,
           ignoreUnchanged=True)
    jobInfo = cjDAO.jobInfo(options.jobID)
    self.logger.info("Job info retrieved: %s" % (str(clippedObj(jobInfo))))


    # ---------------------------------------------------------------------
    # Instantiate the Hypersearch object, which will handle the logic of
    #  which models to create when we need more to evaluate.
    jobParams = json.loads(jobInfo.params)

    # Validate job params
    jsonSchemaPath = os.path.join(os.path.dirname(__file__),
                                  "jsonschema",
                                  "jobParamsSchema.json")
    validate(jobParams, schemaPath=jsonSchemaPath)


    hsVersion = jobParams.get('hsVersion', None)
    if hsVersion == 'v2':
      self._hs = HypersearchV2(searchParams=jobParams, workerID=self._workerID,
              cjDAO=cjDAO, jobID=options.jobID, logLevel=options.logLevel)
    else:
      raise RuntimeError("Invalid Hypersearch implementation (%s) specified" \
                          % (hsVersion))


    # =====================================================================
    # The main loop.
    try:
      exit = False
      numModelsTotal = 0
      print >>sys.stderr, "reporter:status:Evaluating first model..."
      while not exit:

        # ------------------------------------------------------------------
        # Choose a model to evaluate
        batchSize = 10              # How many to try at a time.
        modelIDToRun = None
        while modelIDToRun is None:

          if options.modelID is None:
            # -----------------------------------------------------------------
            # Get the latest results on all running models and send them to
            #  the Hypersearch implementation
            # This calls cjDAO.modelsGetUpdateCounters(), compares the
            # updateCounters with what we have cached, fetches the results for the
            # changed and new models, and sends those to the Hypersearch
            # implementation's self._hs.recordModelProgress() method.
            self._processUpdatedModels(cjDAO)

            # --------------------------------------------------------------------
            # Create a new batch of models
            (exit, newModels) = self._hs.createModels(numModels = batchSize)
            if exit:
              break

            # No more models left to create, just loop. The _hs is waiting for
            #   all remaining running models to complete, and may pick up on an
            #  orphan if it detects one.
            if len(newModels) == 0:
              continue

            # Try and insert one that we will run
            for (modelParams, modelParamsHash, particleHash) in newModels:
              jsonModelParams = json.dumps(modelParams)
              (modelID, ours) = cjDAO.modelInsertAndStart(options.jobID,
                                  jsonModelParams, modelParamsHash, particleHash)

              # Some other worker is already running it, tell the Hypersearch object
              #  so that it doesn't try and insert it again
              if not ours:
                mParamsAndHash = cjDAO.modelsGetParams([modelID])[0]
                mResult = cjDAO.modelsGetResultAndStatus([modelID])[0]
                results = mResult.results
                if results is not None:
                  results = json.loads(results)

                modelParams = json.loads(mParamsAndHash.params)
                particleHash = cjDAO.modelsGetFields(modelID,
                                  ['engParticleHash'])[0]
                particleInst = "%s.%s" % (
                          modelParams['particleState']['id'],
                          modelParams['particleState']['genIdx'])
                self.logger.info("Adding model %d to our internal DB " \
                      "because modelInsertAndStart() failed to insert it: " \
                      "paramsHash=%s, particleHash=%s, particleId='%s'", modelID,
                      mParamsAndHash.engParamsHash.encode('hex'),
                      particleHash.encode('hex'), particleInst)
                self._hs.recordModelProgress(modelID = modelID,
                      modelParams = modelParams,
                      modelParamsHash = mParamsAndHash.engParamsHash,
                      results = results,
                      completed = (mResult.status == cjDAO.STATUS_COMPLETED),
                      completionReason = mResult.completionReason,
                      matured = mResult.engMatured,
                      numRecords = mResult.numRecords)
              else:
                modelIDToRun = modelID
                break

          else:
            # A specific modelID was passed on the command line
            modelIDToRun = int(options.modelID)
            mParamsAndHash = cjDAO.modelsGetParams([modelIDToRun])[0]
            modelParams = json.loads(mParamsAndHash.params)
            modelParamsHash = mParamsAndHash.engParamsHash

            # Make us the worker
            cjDAO.modelSetFields(modelIDToRun,
                                     dict(engWorkerConnId=self._workerID))
            if False:
              # Change the hash and params of the old entry so that we can
              #  create a new model with the same params
              for attempt in range(1000):
                paramsHash = hashlib.md5("OrphanParams.%d.%d" % (modelIDToRun,
                                                                 attempt)).digest()
                particleHash = hashlib.md5("OrphanParticle.%d.%d" % (modelIDToRun,
                                                                  attempt)).digest()
                try:
                  cjDAO.modelSetFields(modelIDToRun,
                                           dict(engParamsHash=paramsHash,
                                                engParticleHash=particleHash))
                  success = True
                except:
                  success = False
                if success:
                  break
              if not success:
                raise RuntimeError("Unexpected failure to change paramsHash and "
                                   "particleHash of orphaned model")

              (modelIDToRun, ours) = cjDAO.modelInsertAndStart(options.jobID,
                                  mParamsAndHash.params, modelParamsHash)



            # ^^^ end while modelIDToRun ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # ---------------------------------------------------------------
        # We have a model, evaluate it now
        # All done?
        if exit:
          break

        # Run the model now
        self.logger.info("RUNNING MODEL GID=%d, paramsHash=%s, params=%s",
              modelIDToRun, modelParamsHash.encode('hex'), modelParams)

        # ---------------------------------------------------------------------
        # Construct model checkpoint GUID for this model:
        # jobParams['persistentJobGUID'] contains the client's (e.g., API Server)
        # persistent, globally-unique model identifier, which is what we need;
        persistentJobGUID = jobParams['persistentJobGUID']
        assert persistentJobGUID, "persistentJobGUID: %r" % (persistentJobGUID,)

        modelCheckpointGUID = jobInfo.client + "_" + persistentJobGUID + (
          '_' + str(modelIDToRun))


        self._hs.runModel(modelID=modelIDToRun, jobID = options.jobID,
                          modelParams=modelParams, modelParamsHash=modelParamsHash,
                          jobsDAO=cjDAO, modelCheckpointGUID=modelCheckpointGUID)

        # TODO: don't increment for orphaned models
        numModelsTotal += 1

        self.logger.info("COMPLETED MODEL GID=%d; EVALUATED %d MODELs",
          modelIDToRun, numModelsTotal)
        print >>sys.stderr, "reporter:status:Evaluated %d models..." % \
                                    (numModelsTotal)
        print >>sys.stderr, "reporter:counter:HypersearchWorker,numModels,1"

        if options.modelID is not None:
          exit = True
        # ^^^ end while not exit

    finally:
      # Provide Hypersearch instance an opportunity to clean up temporary files
      self._hs.close()

    self.logger.info("FINISHED. Evaluated %d models." % (numModelsTotal))
    print >>sys.stderr, "reporter:status:Finished, evaluated %d models" % (numModelsTotal)
    return options.jobID