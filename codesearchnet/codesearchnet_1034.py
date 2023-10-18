def _accumulateFrequencyCounts(values, freqCounts=None):
  """
  Accumulate a list of values 'values' into the frequency counts 'freqCounts',
  and return the updated frequency counts

  For example, if values contained the following: [1,1,3,5,1,3,5], and the initial
  freqCounts was None, then the return value would be:
  [0,3,0,2,0,2]
  which corresponds to how many of each value we saw in the input, i.e. there
  were 0 0's, 3 1's, 0 2's, 2 3's, 0 4's, and 2 5's.

  If freqCounts is not None, the values will be added to the existing counts and
  the length of the frequency Counts will be automatically extended as necessary

  Parameters:
  -----------------------------------------------
  values:         The values to accumulate into the frequency counts
  freqCounts:     Accumulated frequency counts so far, or none
  """

  # How big does our freqCounts vector need to be?
  values = numpy.array(values)
  numEntries = values.max() + 1
  if freqCounts is not None:
    numEntries = max(numEntries, freqCounts.size)

  # Where do we accumulate the results?
  if freqCounts is not None:
    if freqCounts.size != numEntries:
      newCounts = numpy.zeros(numEntries, dtype='int32')
      newCounts[0:freqCounts.size] = freqCounts
    else:
      newCounts = freqCounts
  else:
    newCounts = numpy.zeros(numEntries, dtype='int32')

  # Accumulate the new values
  for v in values:
    newCounts[v] += 1

  return newCounts