def buildOverlappedSequences( numSequences = 2,
                              seqLen = 5,
                              sharedElements = [3,4],
                              numOnBitsPerPattern = 3,
                              patternOverlap = 0,
                              seqOverlap = 0,
                              **kwargs
                              ):
  """ Create training sequences that share some elements in the middle.

  Parameters:
  -----------------------------------------------------
  numSequences:         Number of unique training sequences to generate
  seqLen:               Overall length of each sequence
  sharedElements:       Which element indices of each sequence are shared. These
                          will be in the range between 0 and seqLen-1
  numOnBitsPerPattern:  Number of ON bits in each TM input pattern
  patternOverlap:       Max number of bits of overlap between any 2 patterns
  retval:               (numCols, trainingSequences)
                          numCols - width of the patterns
                          trainingSequences - a list of training sequences

  """

  # Total number of patterns used to build the sequences
  numSharedElements = len(sharedElements)
  numUniqueElements = seqLen - numSharedElements
  numPatterns = numSharedElements + numUniqueElements * numSequences

  # Create the table of patterns
  patterns = getSimplePatterns(numOnBitsPerPattern, numPatterns, patternOverlap)

  # Total number of columns required
  numCols = len(patterns[0])


  # -----------------------------------------------------------------------
  # Create the training sequences
  trainingSequences = []

  uniquePatternIndices = range(numSharedElements, numPatterns)
  for _ in xrange(numSequences):
    sequence = []

    # pattern indices [0 ... numSharedElements-1] are reserved for the shared
    #  middle
    sharedPatternIndices = range(numSharedElements)

    # Build up the sequence
    for j in xrange(seqLen):
      if j in sharedElements:
        patIdx = sharedPatternIndices.pop(0)
      else:
        patIdx = uniquePatternIndices.pop(0)
      sequence.append(patterns[patIdx])

    trainingSequences.append(sequence)


  if VERBOSITY >= 3:
    print "\nTraining sequences"
    printAllTrainingSequences(trainingSequences)

  return (numCols, trainingSequences)