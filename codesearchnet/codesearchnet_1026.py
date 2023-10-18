def vectorsFromSeqList(seqList, patternMatrix):
  """
  Convert a list of sequences of pattern indices, and a pattern lookup table
      into a an array of patterns

  Parameters:
  -----------------------------------------------
  seq:            the sequence, given as indices into the patternMatrix
  patternMatrix:  a SparseMatrix contaning the possible patterns used in
                          the sequence.
  """

  totalLen = 0
  for seq in seqList:
    totalLen += len(seq)

  vectors = numpy.zeros((totalLen, patternMatrix.shape[1]), dtype='bool')
  vecOffset = 0
  for seq in seqList:
    seq = numpy.array(seq, dtype='uint32')
    for idx,coinc in enumerate(seq):
      vectors[vecOffset] = patternMatrix.getRow(int(coinc))
      vecOffset += 1

  return vectors