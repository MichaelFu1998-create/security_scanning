def generateSimpleSequences(nCoinc=10, seqLength=[5,6,7], nSeq=100):
  """
  Generate a set of simple sequences. The elements of the sequences will be
  integers from 0 to 'nCoinc'-1. The length of each sequence will be
  randomly chosen from the 'seqLength' list.

  Parameters:
  -----------------------------------------------
  nCoinc:      the number of elements available to use in the sequences
  seqLength:   a list of possible sequence lengths. The length of each
               sequence will be randomly chosen from here.
  nSeq:        The number of sequences to generate

  retval:      a list of sequences. Each sequence is itself a list
               containing the coincidence indices for that sequence.
  """

  coincList = range(nCoinc)
  seqList  = []

  for i in xrange(nSeq):
    if max(seqLength) <= nCoinc:
      seqList.append(random.sample(coincList, random.choice(seqLength)))
    else:
      len = random.choice(seqLength)
      seq = []
      for x in xrange(len):
        seq.append(random.choice(coincList))
      seqList.append(seq)

  return seqList