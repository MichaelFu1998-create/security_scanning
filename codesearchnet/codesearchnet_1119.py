def recordModelProgress(self, modelID, modelParams, modelParamsHash, results,
                         completed, completionReason, matured, numRecords):
    """Record or update the results for a model. This is called by the
    HSW whenever it gets results info for another model, or updated results
    on a model that is still running.

    The first time this is called for a given modelID, the modelParams will
    contain the params dict for that model and the modelParamsHash will contain
    the hash of the params. Subsequent updates of the same modelID will
    have params and paramsHash values of None (in order to save overhead).

    The Hypersearch object should save these results into it's own working
    memory into some table, which it then uses to determine what kind of
    new models to create next time createModels() is called.

    Parameters:
    ----------------------------------------------------------------------
    modelID:        ID of this model in models table
    modelParams:    params dict for this model, or None if this is just an update
                    of a model that it already previously reported on.

                    See the comments for the createModels() method for a
                    description of this dict.

    modelParamsHash:  hash of the modelParams dict, generated by the worker
                    that put it into the model database.
    results:        tuple containing (allMetrics, optimizeMetric). Each is a
                    dict containing metricName:result pairs. .
                    May be none if we have no results yet.
    completed:      True if the model has completed evaluation, False if it
                      is still running (and these are online results)
    completionReason: One of the ClientJobsDAO.CMPL_REASON_XXX equates
    matured:        True if this model has matured. In most cases, once a
                    model matures, it will complete as well. The only time a
                    model matures and does not complete is if it's currently
                    the best model and we choose to keep it running to generate
                    predictions.
    numRecords:     Number of records that have been processed so far by this
                      model.
    """
    if results is None:
      metricResult = None
    else:
      metricResult = results[1].values()[0]

    # Update our database.
    errScore = self._resultsDB.update(modelID=modelID,
                modelParams=modelParams,modelParamsHash=modelParamsHash,
                metricResult=metricResult, completed=completed,
                completionReason=completionReason, matured=matured,
                numRecords=numRecords)

    # Log message.
    self.logger.debug('Received progress on model %d: completed: %s, '
                      'cmpReason: %s, numRecords: %d, errScore: %s' ,
                      modelID, completed, completionReason, numRecords, errScore)

    # Log best so far.
    (bestModelID, bestResult) = self._resultsDB.bestModelIdAndErrScore()
    self.logger.debug('Best err score seen so far: %s on model %s' % \
                     (bestResult, bestModelID))