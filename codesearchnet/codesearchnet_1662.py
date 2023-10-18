def _updateStatsInferEnd(self, stats, bottomUpNZ, predictedState,
                           colConfidence):
    """
    Called at the end of learning and inference, this routine will update
    a number of stats in our _internalStats dictionary, including our computed
    prediction score.

    :param stats            internal stats dictionary
    :param bottomUpNZ       list of the active bottom-up inputs
    :param predictedState   The columns we predicted on the last time step (should
                            match the current bottomUpNZ in the best case)
    :param colConfidence    Column confidences we determined on the last time step
    """
    # Return if not collecting stats
    if not self.collectStats:
      return
    stats['nInfersSinceReset'] += 1

    # Compute the prediction score, how well the prediction from the last
    # time step predicted the current bottom-up input
    (numExtra2, numMissing2, confidences2) = self._checkPrediction(
        patternNZs=[bottomUpNZ], output=predictedState,
        colConfidence=colConfidence)
    predictionScore, positivePredictionScore, negativePredictionScore = (
        confidences2[0])

    # Store the stats that don't depend on burn-in
    stats['curPredictionScore2'] = float(predictionScore)
    stats['curFalseNegativeScore'] = 1.0 - float(positivePredictionScore)
    stats['curFalsePositiveScore'] = float(negativePredictionScore)

    stats['curMissing'] = numMissing2
    stats['curExtra'] = numExtra2

    # If we are passed the burn-in period, update the accumulated stats
    # Here's what various burn-in values mean:
    #   0: try to predict the first element of each sequence and all subsequent
    #   1: try to predict the second element of each sequence and all subsequent
    #   etc.
    if stats['nInfersSinceReset'] <= self.burnIn:
      return

    # Burn-in related stats
    stats['nPredictions'] += 1
    numExpected = max(1.0, float(len(bottomUpNZ)))

    stats['totalMissing'] += numMissing2
    stats['totalExtra'] += numExtra2
    stats['pctExtraTotal'] += 100.0 * numExtra2 / numExpected
    stats['pctMissingTotal'] += 100.0 * numMissing2 / numExpected
    stats['predictionScoreTotal2'] += float(predictionScore)
    stats['falseNegativeScoreTotal'] += 1.0 - float(positivePredictionScore)
    stats['falsePositiveScoreTotal'] += float(negativePredictionScore)

    if self.collectSequenceStats:
      # Collect cell confidences for every cell that correctly predicted current
      # bottom up input. Normalize confidence across each column
      cc = self.cellConfidence['t-1'] * self.infActiveState['t']
      sconf = cc.sum(axis=1)
      for c in range(self.numberOfCols):
        if sconf[c] > 0:
          cc[c, :] /= sconf[c]

      # Update cell confidence histogram: add column-normalized confidence
      # scores to the histogram
      self._internalStats['confHistogram'] += cc