def generateHubSequences(nCoinc=10, hubs = [2,6], seqLength=[5,6,7], nSeq=100):
  """
  Generate a set of hub sequences. These are sequences which contain a hub
  element in the middle. The elements of the sequences will be integers
  from 0 to 'nCoinc'-1. The hub elements will only appear in the middle of
  each sequence. The length of each sequence will be randomly chosen from the
  'seqLength' list.

  Parameters:
  -----------------------------------------------
  nCoinc:        the number of elements available to use in the sequences
  hubs:          which of the elements will be used as hubs.
  seqLength:     a list of possible sequence lengths. The length of each
                        sequence will be randomly chosen from here.
  nSeq:          The number of sequences to generate

  retval:        a list of sequences. Each sequence is itself a list
                containing the coincidence indices for that sequence.
  """


  coincList = range(nCoinc)
  for hub in hubs:
    coincList.remove(hub)

  seqList = []
  for i in xrange(nSeq):
    length = random.choice(seqLength)-1
    seq = random.sample(coincList,length)
    seq.insert(length//2, random.choice(hubs))
    seqList.append(seq)

  return seqList