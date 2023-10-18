def generateSequences(nPatterns=10, patternLen=500, patternActivity=50,
                    hubs=[2,6],  seqLength=[5,6,7],
                    nSimpleSequences=50,  nHubSequences=50):
  """
  Generate a set of simple and hub sequences. A simple sequence contains
  a randomly chosen set of elements from 0 to 'nCoinc-1'. A hub sequence
  always contains a hub element in the middle of it.

  Parameters:
  -----------------------------------------------
  nPatterns:        the number of patterns to use in the sequences.
  patternLen:       The number of elements in each pattern
  patternActivity:  The number of elements that should be active in
                        each pattern
  hubs:             which of the elements will be used as hubs.
  seqLength:        a list of possible sequence lengths. The length of each
                        sequence will be randomly chosen from here.
  nSimpleSequences: The number of simple sequences to generate
  nHubSequences:    The number of hub sequences to generate

  retval:           (seqList, patterns)
                    seqList: a list of sequences. Each sequence is itself a list
                                  containing the input pattern indices for that sequence.
                    patterns: the input patterns used in the seqList.
  """

  # Create the input patterns
  patterns = generateCoincMatrix(nCoinc=nPatterns, length=patternLen,
              activity=patternActivity)

  # Create the raw sequences
  seqList =  generateSimpleSequences(nCoinc=nPatterns, seqLength=seqLength,
                                    nSeq=nSimpleSequences) + \
             generateHubSequences(nCoinc=nPatterns, hubs=hubs, seqLength=seqLength,
                                  nSeq=nHubSequences)

  # Return results
  return (seqList, patterns)