def buildSequencePool(numSequences = 10,
                      seqLen = [2,3,4],
                      numPatterns = 5,
                      numOnBitsPerPattern = 3,
                      patternOverlap = 0,
                      **kwargs
                      ):
  """ Create a bunch of sequences of various lengths, all built from
  a fixed set of patterns.

  Parameters:
  -----------------------------------------------------
  numSequences:         Number of training sequences to generate
  seqLen:               List of possible sequence lengths
  numPatterns:          How many possible patterns there are to use within
                          sequences
  numOnBitsPerPattern:  Number of ON bits in each TM input pattern
  patternOverlap:       Max number of bits of overlap between any 2 patterns
  retval:               (numCols, trainingSequences)
                          numCols - width of the patterns
                          trainingSequences - a list of training sequences

  """


  # Create the table of patterns
  patterns = getSimplePatterns(numOnBitsPerPattern, numPatterns, patternOverlap)

  # Total number of columns required
  numCols = len(patterns[0])


  # -----------------------------------------------------------------------
  # Create the training sequences
  trainingSequences = []
  for _ in xrange(numSequences):

    # Build it up from patterns
    sequence = []
    length = random.choice(seqLen)
    for _ in xrange(length):
      patIdx = random.choice(xrange(numPatterns))
      sequence.append(patterns[patIdx])

    # Put it in
    trainingSequences.append(sequence)


  if VERBOSITY >= 3:
    print "\nTraining sequences"
    printAllTrainingSequences(trainingSequences)

  return (numCols, trainingSequences)