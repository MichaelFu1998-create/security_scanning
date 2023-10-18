def _aggr_sum(inList):
  """ Returns sum of the elements in the list. Missing items are replaced with
  the mean value
  """
  aggrMean = _aggr_mean(inList)
  if aggrMean == None:
    return None

  aggrSum = 0
  for elem in inList:
    if elem != SENTINEL_VALUE_FOR_MISSING_DATA:
      aggrSum += elem
    else:
      aggrSum += aggrMean

  return aggrSum