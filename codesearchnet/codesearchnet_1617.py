def _processUpdatedModels(self, cjDAO):
    """ For all models that modified their results since last time this method
    was called, send their latest results to the Hypersearch implementation.
    """


    # Get the latest update counters. This returns a list of tuples:
    #  (modelID, updateCounter)
    curModelIDCtrList = cjDAO.modelsGetUpdateCounters(self._options.jobID)
    if len(curModelIDCtrList) == 0:
      return

    self.logger.debug("current modelID/updateCounters: %s" \
                      % (str(curModelIDCtrList)))
    self.logger.debug("last modelID/updateCounters: %s" \
                      % (str(self._modelIDCtrList)))

    # --------------------------------------------------------------------
    # Find out which ones have changed update counters. Since these are models
    # that the Hypersearch implementation already knows about, we don't need to
    # send params or paramsHash
    curModelIDCtrList = sorted(curModelIDCtrList)
    numItems = len(curModelIDCtrList)

    # Each item in the list we are filtering contains:
    #  (idxIntoModelIDCtrList, (modelID, curCtr), (modelID, oldCtr))
    # We only want to keep the ones where the oldCtr != curCtr
    changedEntries = filter(lambda x:x[1][1] != x[2][1],
                      itertools.izip(xrange(numItems), curModelIDCtrList,
                                     self._modelIDCtrList))

    if len(changedEntries) > 0:
      # Update values in our cache
      self.logger.debug("changedEntries: %s", str(changedEntries))
      for entry in changedEntries:
        (idx, (modelID, curCtr), (_, oldCtr)) = entry
        self._modelIDCtrDict[modelID] = curCtr
        assert (self._modelIDCtrList[idx][0] == modelID)
        assert (curCtr != oldCtr)
        self._modelIDCtrList[idx][1] = curCtr


      # Tell Hypersearch implementation of the updated results for each model
      changedModelIDs = [x[1][0] for x in changedEntries]
      modelResults = cjDAO.modelsGetResultAndStatus(changedModelIDs)
      for mResult in modelResults:
        results = mResult.results
        if results is not None:
          results = json.loads(results)
        self._hs.recordModelProgress(modelID=mResult.modelId,
                     modelParams = None,
                     modelParamsHash = mResult.engParamsHash,
                     results = results,
                     completed = (mResult.status == cjDAO.STATUS_COMPLETED),
                     completionReason = mResult.completionReason,
                     matured = mResult.engMatured,
                     numRecords = mResult.numRecords)

    # --------------------------------------------------------------------
    # Figure out which ones are newly arrived and add them to our
    #   cache
    curModelIDSet = set([x[0] for x in curModelIDCtrList])
    newModelIDs = curModelIDSet.difference(self._modelIDSet)
    if len(newModelIDs) > 0:

      # Add new modelID and counters to our cache
      self._modelIDSet.update(newModelIDs)
      curModelIDCtrDict = dict(curModelIDCtrList)

      # Get the results for each of these models and send them to the
      #  Hypersearch implementation.
      modelInfos = cjDAO.modelsGetResultAndStatus(newModelIDs)
      modelInfos.sort()
      modelParamsAndHashs = cjDAO.modelsGetParams(newModelIDs)
      modelParamsAndHashs.sort()

      for (mResult, mParamsAndHash) in itertools.izip(modelInfos,
                                                  modelParamsAndHashs):

        modelID = mResult.modelId
        assert (modelID == mParamsAndHash.modelId)

        # Update our cache of IDs and update counters
        self._modelIDCtrDict[modelID] = curModelIDCtrDict[modelID]
        self._modelIDCtrList.append([modelID, curModelIDCtrDict[modelID]])

        # Tell the Hypersearch implementation of the new model
        results = mResult.results
        if results is not None:
          results = json.loads(mResult.results)

        self._hs.recordModelProgress(modelID = modelID,
            modelParams = json.loads(mParamsAndHash.params),
            modelParamsHash = mParamsAndHash.engParamsHash,
            results = results,
            completed = (mResult.status == cjDAO.STATUS_COMPLETED),
            completionReason = (mResult.completionReason),
            matured = mResult.engMatured,
            numRecords = mResult.numRecords)




      # Keep our list sorted
      self._modelIDCtrList.sort()