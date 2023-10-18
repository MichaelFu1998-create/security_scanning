def getSimplePatterns(numOnes, numPatterns, patternOverlap=0):
  """Very simple patterns. Each pattern has numOnes consecutive
  bits on. The amount of overlap between consecutive patterns is
  configurable, via the patternOverlap parameter.

  Parameters:
  -----------------------------------------------------------------------
  numOnes:        Number of bits ON in each pattern
  numPatterns:    Number of unique patterns to generate
  patternOverlap: Number of bits of overlap between each successive pattern
  retval:         patterns
  """

  assert (patternOverlap < numOnes)

  # How many new bits are introduced in each successive pattern?
  numNewBitsInEachPattern = numOnes - patternOverlap
  numCols = numNewBitsInEachPattern * numPatterns + patternOverlap

  p = []
  for i in xrange(numPatterns):
    x = numpy.zeros(numCols, dtype='float32')

    startBit = i*numNewBitsInEachPattern
    nextStartBit = startBit + numOnes
    x[startBit:nextStartBit] = 1

    p.append(x)

  return p