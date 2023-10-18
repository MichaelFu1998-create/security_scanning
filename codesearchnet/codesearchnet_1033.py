def removeSeqStarts(vectors, resets, numSteps=1):
  """
  Convert a list of sequences of pattern indices, and a pattern lookup table
      into a an array of patterns

  Parameters:
  -----------------------------------------------
  vectors:          the data vectors. Row 0 contains the outputs from time
                    step 0, row 1 from time step 1, etc.
  resets:           the reset signal. This is a vector of booleans
                    the same length as the number of rows in 'vectors'. It
                    has a 1 where a sequence started and a 0 otherwise. The
                    first 'numSteps' rows of 'vectors' of each sequence will
                    not be included in the return result.
  numSteps          Number of samples to remove from the start of each sequence

  retval:           copy of vectors, with the first 'numSteps' samples at the
                    start of each sequence removed.
  """

  # Do nothing if numSteps is 0
  if numSteps == 0:
    return vectors

  resetIndices = resets.nonzero()[0]
  removeRows = resetIndices
  for i in range(numSteps-1):
    removeRows = numpy.hstack((removeRows, resetIndices+i+1))

  return numpy.delete(vectors, removeRows, axis=0)