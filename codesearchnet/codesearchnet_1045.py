def predictionExtent(inputs, resets, outputs, minOverlapPct=100.0):
  """
  Computes the predictive ability of a temporal memory (TM). This routine returns
  a value which is the average number of time steps of prediction provided
  by the TM. It accepts as input the inputs, outputs, and resets provided to
  the TM as well as a 'minOverlapPct' used to evalulate whether or not a
  prediction is a good enough match to the actual input.

  The 'outputs' are the pooling outputs of the TM. This routine treats each output
  as a "manifold" that includes the active columns that should be present in the
  next N inputs. It then looks at each successive input and sees if it's active
  columns are within the manifold. For each output sample, it computes how
  many time steps it can go forward on the input before the input overlap with
  the manifold is less then 'minOverlapPct'. It returns the average number of
  time steps calculated for each output.

  Parameters:
  -----------------------------------------------
  inputs:          The inputs to the TM. Row 0 contains the inputs from time
                   step 0, row 1 from time step 1, etc.
  resets:          The reset input to the TM. Element 0 contains the reset from
                   time step 0, element 1 from time step 1, etc.
  outputs:         The pooling outputs from the TM. Row 0 contains the outputs
                   from time step 0, row 1 from time step 1, etc.
  minOverlapPct:   How much each input's columns must overlap with the pooling
                   output's columns to be considered a valid prediction.

  retval:          (Average number of time steps of prediction over all output
                     samples,
                    Average number of time steps of prediction when we aren't
                     cut short by the end of the sequence,
                    List containing frequency counts of each encountered
                     prediction time)

  """

  # List of how many times we encountered each prediction amount. Element 0
  #  is how many times we successfully predicted 0 steps in advance, element 1
  #  is how many times we predicted 1 step in advance, etc.
  predCounts = None

  # Total steps of prediction over all samples
  predTotal = 0

  # Total number of samples
  nSamples = len(outputs)

  # Total steps of prediction for samples at the start of the sequence, or
  #  for samples whose prediction runs aren't cut short by the end of the
  #  sequence.
  predTotalNotLimited = 0
  nSamplesNotLimited = 0

  # Compute how many cells/column we have
  nCols = len(inputs[0])
  nCellsPerCol = len(outputs[0]) // nCols

  # Evalulate prediction for each output sample
  for idx in xrange(nSamples):

    # What are the active columns for this output?
    activeCols = outputs[idx].reshape(nCols, nCellsPerCol).max(axis=1)

    # How many steps of prediction do we have?
    steps = 0
    while (idx+steps+1 < nSamples) and (resets[idx+steps+1] == 0):
      overlap = numpy.logical_and(inputs[idx+steps+1], activeCols)
      overlapPct = 100.0 * float(overlap.sum()) / inputs[idx+steps+1].sum()
      if overlapPct >= minOverlapPct:
        steps += 1
      else:
        break

    # print "idx:", idx, "steps:", steps
    # Accumulate into our total
    predCounts = _accumulateFrequencyCounts([steps], predCounts)
    predTotal += steps

    # If this sample was not cut short by the end of the sequence, include
    #  it into the "NotLimited" runs
    if resets[idx] or \
        ((idx+steps+1 < nSamples) and (not resets[idx+steps+1])):
      predTotalNotLimited += steps
      nSamplesNotLimited += 1

  # Return results
  return (float(predTotal) / nSamples,
          float(predTotalNotLimited) / nSamplesNotLimited,
          predCounts)