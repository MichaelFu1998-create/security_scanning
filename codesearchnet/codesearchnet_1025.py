def generateL2Sequences(nL1Patterns=10, l1Hubs=[2,6], l1SeqLength=[5,6,7],
                  nL1SimpleSequences=50,  nL1HubSequences=50,
                  l1Pooling=4, perfectStability=False, spHysteresisFactor=1.0,
                  patternLen=500, patternActivity=50):
  """
  Generate the simulated output from a spatial pooler that's sitting
  on top of another spatial pooler / temporal memory pair.  The average on-time
  of the outputs from the simulated TM is given by the l1Pooling argument.

  In this routine, L1 refers to the first spatial and temporal memory and L2
  refers to the spatial pooler above that.

  Parameters:
  -----------------------------------------------
  nL1Patterns:          the number of patterns to use in the L1 sequences.
  l1Hubs:               which of the elements will be used as hubs.
  l1SeqLength:          a list of possible sequence lengths. The length of each
                        sequence will be randomly chosen from here.
  nL1SimpleSequences:   The number of simple sequences to generate for L1
  nL1HubSequences:      The number of hub sequences to generate for L1
  l1Pooling:            The number of time steps to pool over in the L1 temporal
                          pooler
  perfectStability:     If true, then the input patterns represented by the
                        sequences generated will have perfect stability over
                        l1Pooling time steps. This is the best case ideal input
                        to a TM. In actual situations, with an actual SP
                        providing input, the stability will always be less than
                        this.
  spHystereisFactor:    The hysteresisFactor to use in the L2 spatial pooler.
                        Only used when perfectStability is  False
  patternLen:           The number of elements in each pattern output by L2
  patternActivity:      The number of elements that should be active in
                        each pattern

  @retval:              (seqList, patterns)
                        seqList: a list of sequences output from L2. Each sequence is
                            itself a list containing the input pattern indices for that
                            sequence.
                        patterns: the input patterns used in the L2 seqList.
  """

  # First, generate the L1 sequences
  l1SeqList = generateSimpleSequences(nCoinc=nL1Patterns, seqLength=l1SeqLength,
                                    nSeq=nL1SimpleSequences) + \
             generateHubSequences(nCoinc=nL1Patterns, hubs=l1Hubs,
                                    seqLength=l1SeqLength, nSeq=nL1HubSequences)

  # Generate the L2 SP output from those
  spOutput = generateSlowSPOutput(seqListBelow = l1SeqList,
                poolingTimeBelow=l1Pooling, outputWidth=patternLen,
                activity=patternActivity, perfectStability=perfectStability,
                spHysteresisFactor=spHysteresisFactor)

  # Map the spOutput patterns into indices into a pattern matrix which we
  #  generate now.
  outSeq = None
  outSeqList = []
  outPatterns = SM32(0, patternLen)
  for pattern in spOutput:
    # If we have a reset vector start a new sequence
    if pattern.sum() == 0:
      if outSeq is not None:
        outSeqList.append(outSeq)
      outSeq = []
      continue

    # See if this vector matches a pattern we've already seen before
    patternIdx = None
    if outPatterns.nRows() > 0:
      # Find most matching 1's.
      matches = outPatterns.rightVecSumAtNZ(pattern)
      outCoinc = matches.argmax().astype('uint32')
      # See if its number of 1's is the same in the pattern and in the
      #  coincidence row. If so, it is an exact match
      numOnes = pattern.sum()
      if matches[outCoinc] == numOnes \
          and outPatterns.getRow(int(outCoinc)).sum() == numOnes:
        patternIdx = outCoinc

    # If no match, add this pattern to our matrix
    if patternIdx is None:
      outPatterns.addRow(pattern)
      patternIdx = outPatterns.nRows() - 1

    # Store the pattern index into the sequence
    outSeq.append(patternIdx)

  # Put in last finished sequence
  if outSeq is not None:
    outSeqList.append(outSeq)

  # Return with the seqList and patterns matrix
  return (outSeqList, outPatterns)