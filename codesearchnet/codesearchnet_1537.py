def _aggr_weighted_mean(inList, params):
  """ Weighted mean uses params (must be the same size as inList) and
  makes weighed mean of inList"""
  assert(len(inList) == len(params))

  # If all weights are 0, then the value is not defined, return None (missing)
  weightsSum = sum(params)
  if weightsSum == 0:
    return None

  weightedMean = 0
  for i, elem in enumerate(inList):
    weightedMean += elem * params[i]

  return weightedMean / weightsSum