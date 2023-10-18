def getFieldContributions(self):
    """Return the field contributions statistics.

    Parameters:
    ---------------------------------------------------------------------
    retval:   Dictionary where the keys are the field names and the values
                are how much each field contributed to the best score.
    """

    #in the fast swarm, there is only 1 sprint and field contributions are
    #not defined
    if self._hsObj._fixedFields is not None:
      return dict(), dict()
    # Get the predicted field encoder name
    predictedEncoderName = self._hsObj._predictedFieldEncoder

    # -----------------------------------------------------------------------
    # Collect all the single field scores
    fieldScores = []
    for swarmId, info in self._state['swarms'].iteritems():
      encodersUsed = swarmId.split('.')
      if len(encodersUsed) != 1:
        continue
      field = self.getEncoderNameFromKey(encodersUsed[0])
      bestScore = info['bestErrScore']

      # If the bestScore is None, this swarm hasn't completed yet (this could
      #  happen if we're exiting because of maxModels), so look up the best
      #  score so far
      if bestScore is None:
        (_modelId, bestScore) = \
            self._hsObj._resultsDB.bestModelIdAndErrScore(swarmId)

      fieldScores.append((bestScore, field))


    # -----------------------------------------------------------------------
    # If we only have 1 field that was tried in the first sprint, then use that
    #  as the base and get the contributions from the fields in the next sprint.
    if self._hsObj._searchType == HsSearchType.legacyTemporal:
      assert(len(fieldScores)==1)
      (baseErrScore, baseField) = fieldScores[0]

      for swarmId, info in self._state['swarms'].iteritems():
        encodersUsed = swarmId.split('.')
        if len(encodersUsed) != 2:
          continue

        fields = [self.getEncoderNameFromKey(name) for name in encodersUsed]
        fields.remove(baseField)

        fieldScores.append((info['bestErrScore'], fields[0]))

    # The first sprint tried a bunch of fields, pick the worst performing one
    #  (within the top self._hsObj._maxBranching ones) as the base
    else:
      fieldScores.sort(reverse=True)

      # If maxBranching was specified, pick the worst performing field within
      #  the top maxBranching+1 fields as our base, which will give that field
      #  a contribution of 0.
      if self._hsObj._maxBranching > 0 \
              and len(fieldScores) > self._hsObj._maxBranching:
        baseErrScore = fieldScores[-self._hsObj._maxBranching-1][0]
      else:
        baseErrScore = fieldScores[0][0]


    # -----------------------------------------------------------------------
    # Prepare and return the fieldContributions dict
    pctFieldContributionsDict = dict()
    absFieldContributionsDict = dict()

    # If we have no base score, can't compute field contributions. This can
    #  happen when we exit early due to maxModels or being cancelled
    if baseErrScore is not None:

      # If the base error score is 0, we can't compute a percent difference
      #  off of it, so move it to a very small float
      if abs(baseErrScore) < 0.00001:
        baseErrScore = 0.00001
      for (errScore, field) in fieldScores:
        if errScore is not None:
          pctBetter = (baseErrScore - errScore) * 100.0 / baseErrScore
        else:
          pctBetter = 0.0
          errScore = baseErrScore   # for absFieldContribution

        pctFieldContributionsDict[field] = pctBetter
        absFieldContributionsDict[field] = baseErrScore - errScore

    self.logger.debug("FieldContributions: %s" % (pctFieldContributionsDict))
    return pctFieldContributionsDict, absFieldContributionsDict