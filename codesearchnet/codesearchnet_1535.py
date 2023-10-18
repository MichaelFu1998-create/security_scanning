def _aggr_mean(inList):
  """ Returns mean of non-None elements of the list
  """
  aggrSum = 0
  nonNone = 0
  for elem in inList:
    if elem != SENTINEL_VALUE_FOR_MISSING_DATA:
      aggrSum += elem
      nonNone += 1
  if nonNone != 0:
    return aggrSum / nonNone
  else:
    return None