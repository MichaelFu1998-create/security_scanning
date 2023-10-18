def averageOnTimePerTimestep(vectors, numSamples=None):
  """
  Computes the average on-time of the outputs that are on at each time step, and
  then averages this over all time steps.

  This metric is resiliant to the number of outputs that are on at each time
  step. That is, if time step 0 has many more outputs on than time step 100, it
  won't skew the results. This is particularly useful when measuring the
  average on-time of things like the temporal memory output where you might
  have many columns bursting at the start of a sequence - you don't want those
  start of sequence bursts to over-influence the calculated average on-time.

  Parameters:
  -----------------------------------------------
  vectors:          the vectors for which the onTime is calculated. Row 0
                    contains the outputs from time step 0, row 1 from time step
                    1, etc.
  numSamples:       the number of elements for which on-time is calculated.
                    If not specified, then all elements are looked at.

  Returns  (scalar average on-time over all time steps,
            list containing frequency counts of each encountered on-time)

  """


  # Special case given a 1 dimensional vector: it represents a single column
  if vectors.ndim == 1:
    vectors.shape = (-1,1)
  numTimeSteps = len(vectors)
  numElements  = len(vectors[0])

  # How many samples will we look at?
  if numSamples is not None:
    import pdb; pdb.set_trace()   # Test this....
    countOn    = numpy.random.randint(0, numElements, numSamples)
    vectors = vectors[:, countOn]

  # Fill in each non-zero of vectors with the on-time that that output was
  #  on for.
  durations = numpy.zeros(vectors.shape, dtype='int32')
  for col in xrange(vectors.shape[1]):
    _fillInOnTimes(vectors[:,col], durations[:,col])

  # Compute the average on time for each time step
  sums = vectors.sum(axis=1)
  sums.clip(min=1, max=numpy.inf, out=sums)
  avgDurations = durations.sum(axis=1, dtype='float64') / sums
  avgOnTime = avgDurations.sum() / (avgDurations > 0).sum()

  # Generate the frequency counts for each duration
  freqCounts = _accumulateFrequencyCounts(avgDurations)
  return (avgOnTime, freqCounts)