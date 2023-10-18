def _removeUnlikelyPredictions(cls, likelihoodsDict, minLikelihoodThreshold,
                                 maxPredictionsPerStep):
    """Remove entries with 0 likelihood or likelihood less than
    minLikelihoodThreshold, but don't leave an empty dict.
    """
    maxVal = (None, None)
    for (k, v) in likelihoodsDict.items():
      if len(likelihoodsDict) <= 1:
        break
      if maxVal[0] is None or v >= maxVal[1]:
        if maxVal[0] is not None and maxVal[1] < minLikelihoodThreshold:
          del likelihoodsDict[maxVal[0]]
        maxVal = (k, v)
      elif v < minLikelihoodThreshold:
        del likelihoodsDict[k]
    # Limit the number of predictions to include.
    likelihoodsDict = dict(sorted(likelihoodsDict.iteritems(),
                                  key=itemgetter(1),
                                  reverse=True)[:maxPredictionsPerStep])
    return likelihoodsDict