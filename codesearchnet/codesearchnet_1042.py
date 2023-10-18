def percentOutputsStableOverNTimeSteps(vectors, numSamples=None):
  """
  Returns the percent of the outputs that remain completely stable over
  N time steps.

  Parameters:
  -----------------------------------------------
  vectors:        the vectors for which the stability is calculated
  numSamples:     the number of time steps where stability is counted

  For each window of numSamples, count how many outputs are active during
  the entire window.

  """

  # ----------------------------------------------------------------------
  # Calculate the stability
  totalSamples = len(vectors)
  windowSize = numSamples

  # Process each window
  numWindows = 0
  pctStable = 0

  for wStart in range(0, totalSamples-windowSize+1):
    # Count how many elements are active for the entire time
    data = vectors[wStart:wStart+windowSize]
    outputSums = data.sum(axis=0)
    stableOutputs = (outputSums == windowSize).sum()

    # Accumulated
    samplePctStable = float(stableOutputs) / data[0].sum()
    print samplePctStable
    pctStable += samplePctStable
    numWindows += 1

  # Return percent average over all possible windows
  return float(pctStable) / numWindows