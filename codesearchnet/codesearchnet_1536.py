def _aggr_mode(inList):
  """ Returns most common value seen in the non-None elements of the list
  """

  valueCounts = dict()
  nonNone = 0

  for elem in inList:
    if elem == SENTINEL_VALUE_FOR_MISSING_DATA:
      continue

    nonNone += 1
    if elem in valueCounts:
      valueCounts[elem] += 1
    else:
      valueCounts[elem] = 1

  # Get the most common one
  if nonNone == 0:
    return None

  # Sort by counts
  sortedCounts = valueCounts.items()
  sortedCounts.sort(cmp=lambda x,y: x[1] - y[1], reverse=True)
  return sortedCounts[0][0]