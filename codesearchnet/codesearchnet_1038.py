def averageOnTime(vectors, numSamples=None):
  """
  Returns the average on-time, averaged over all on-time runs.

  Parameters:
  -----------------------------------------------
  vectors:          the vectors for which the onTime is calculated. Row 0
                    contains the outputs from time step 0, row 1 from time step
                    1, etc.
  numSamples:       the number of elements for which on-time is calculated.
                    If not specified, then all elements are looked at.

  Returns:    (scalar average on-time of all outputs,
               list containing frequency counts of each encountered on-time)


  """

  # Special case given a 1 dimensional vector: it represents a single column
  if vectors.ndim == 1:
    vectors.shape = (-1,1)
  numTimeSteps = len(vectors)
  numElements  = len(vectors[0])

  # How many samples will we look at?
  if numSamples is None:
    numSamples = numElements
    countOn    = range(numElements)
  else:
    countOn    = numpy.random.randint(0, numElements, numSamples)

  # Compute the on-times and accumulate the frequency counts of each on-time
  #  encountered
  sumOfLengths = 0.0
  onTimeFreqCounts = None
  n = 0
  for i in countOn:
    (onTime, segments, durations) = _listOfOnTimesInVec(vectors[:,i])
    if onTime != 0.0:
      sumOfLengths += onTime
      n += segments
      onTimeFreqCounts = _accumulateFrequencyCounts(durations, onTimeFreqCounts)

  # Return the average on time of each element that was on.
  if n > 0:
    return (sumOfLengths/n, onTimeFreqCounts)
  else:
    return (0.0, onTimeFreqCounts)