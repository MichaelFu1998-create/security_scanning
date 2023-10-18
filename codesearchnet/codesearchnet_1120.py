def runModel(self, modelID, jobID, modelParams, modelParamsHash,
               jobsDAO, modelCheckpointGUID):
    """Run the given model.

    This runs the model described by 'modelParams'. Periodically, it updates
    the results seen on the model to the model database using the databaseAO
    (database Access Object) methods.

    Parameters:
    -------------------------------------------------------------------------
    modelID:             ID of this model in models table

    jobID:               ID for this hypersearch job in the jobs table

    modelParams:         parameters of this specific model
                         modelParams is a dictionary containing the name/value
                         pairs of each variable we are permuting over. Note that
                         variables within an encoder spec have their name
                         structure as:
                           <encoderName>.<encodrVarName>

    modelParamsHash:     hash of modelParamValues

    jobsDAO              jobs data access object - the interface to the jobs
                          database where model information is stored

    modelCheckpointGUID: A persistent, globally-unique identifier for
                          constructing the model checkpoint key
    """

    # We're going to make an assumption that if we're not using streams, that
    #  we also don't need checkpoints saved. For now, this assumption is OK
    #  (if there are no streams, we're typically running on a single machine
    #  and just save models to files) but we may want to break this out as
    #  a separate controllable parameter in the future
    if not self._createCheckpoints:
      modelCheckpointGUID = None

    # Register this model in our database
    self._resultsDB.update(modelID=modelID,
                           modelParams=modelParams,
                           modelParamsHash=modelParamsHash,
                           metricResult = None,
                           completed = False,
                           completionReason = None,
                           matured = False,
                           numRecords = 0)

    # Get the structured params, which we pass to the base description
    structuredParams = modelParams['structuredParams']

    if self.logger.getEffectiveLevel() <= logging.DEBUG:
      self.logger.debug("Running Model. \nmodelParams: %s, \nmodelID=%s, " % \
                        (pprint.pformat(modelParams, indent=4), modelID))

    # Record time.clock() so that we can report on cpu time
    cpuTimeStart = time.clock()

    # Run the experiment. This will report the results back to the models
    #  database for us as well.
    logLevel = self.logger.getEffectiveLevel()
    try:
      if self._dummyModel is None or self._dummyModel is False:
        (cmpReason, cmpMsg) = runModelGivenBaseAndParams(
                    modelID=modelID,
                    jobID=jobID,
                    baseDescription=self._baseDescription,
                    params=structuredParams,
                    predictedField=self._predictedField,
                    reportKeys=self._reportKeys,
                    optimizeKey=self._optimizeKey,
                    jobsDAO=jobsDAO,
                    modelCheckpointGUID=modelCheckpointGUID,
                    logLevel=logLevel,
                    predictionCacheMaxRecords=self._predictionCacheMaxRecords)
      else:
        dummyParams = dict(self._dummyModel)
        dummyParams['permutationParams'] = structuredParams
        if self._dummyModelParamsFunc is not None:
          permInfo = dict(structuredParams)
          permInfo ['generation'] = modelParams['particleState']['genIdx']
          dummyParams.update(self._dummyModelParamsFunc(permInfo))

        (cmpReason, cmpMsg) = runDummyModel(
                      modelID=modelID,
                      jobID=jobID,
                      params=dummyParams,
                      predictedField=self._predictedField,
                      reportKeys=self._reportKeys,
                      optimizeKey=self._optimizeKey,
                      jobsDAO=jobsDAO,
                      modelCheckpointGUID=modelCheckpointGUID,
                      logLevel=logLevel,
                      predictionCacheMaxRecords=self._predictionCacheMaxRecords)

      # Write out the completion reason and message
      jobsDAO.modelSetCompleted(modelID,
                            completionReason = cmpReason,
                            completionMsg = cmpMsg,
                            cpuTime = time.clock() - cpuTimeStart)


    except InvalidConnectionException, e:
      self.logger.warn("%s", e)