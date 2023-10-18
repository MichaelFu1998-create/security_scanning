def populationStability(vectors, numSamples=None):
  """
  Returns the stability for the population averaged over multiple time steps

  Parameters:
  -----------------------------------------------
  vectors:          the vectors for which the stability is calculated
  numSamples        the number of time steps where stability is counted

  At each time step, count the fraction of the active elements which are stable
  from the previous step
  Average all the fraction

  """

  # ----------------------------------------------------------------------
  # Calculate the stability
  numVectors = len(vectors)

  if numSamples is None:
    numSamples = numVectors-1
    countOn = range(numVectors-1)
  else:
    countOn = numpy.random.randint(0, numVectors-1, numSamples)


  sigmap = 0.0
  for i in countOn:
    match = checkMatch(vectors[i], vectors[i+1], sparse=False)
    # Ignore reset vectors (all 0's)
    if match[1] != 0:
      sigmap += float(match[0])/match[1]

  return sigmap / numSamples