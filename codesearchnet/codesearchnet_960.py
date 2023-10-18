def _generateOverlapping(filename="overlap.csv", numSequences=2, elementsPerSeq=3, 
                    numRepeats=10, hub=[0,1], hubOffset=1, resets=False):
  
  """ Generate a temporal dataset containing sequences that overlap one or more
  elements with other sequences. 
  
  Parameters:
  ----------------------------------------------------
  filename:       name of the file to produce, including extension. It will
                  be created in a 'datasets' sub-directory within the 
                  directory containing this script. 
  numSequences:   how many sequences to generate
  elementsPerSeq: length of each sequence
  numRepeats:     how many times to repeat each sequence in the output 
  hub:            sub-sequence to place within each other sequence 
  hubOffset:      where, within each sequence, to place the hub
  resets:         if True, turn on reset at start of each sequence
  """
  
  # Check for conflicts in arguments
  assert (hubOffset + len(hub) <= elementsPerSeq)
  
  # Create the output file
  scriptDir = os.path.dirname(__file__)
  pathname = os.path.join(scriptDir, 'datasets', filename)
  print "Creating %s..." % (pathname)
  fields = [('reset', 'int', 'R'), 
            ('field1', 'string', ''),  
            ('field2', 'float', '')]  
  outFile = FileRecordStream(pathname, write=True, fields=fields)
  

  # Create the sequences with the hub in the middle
  sequences = []
  nextElemIdx = max(hub)+1
  
  for _ in range(numSequences):
    seq = []
    for j in range(hubOffset):
      seq.append(nextElemIdx)
      nextElemIdx += 1
    for j in hub:
      seq.append(j)
    j = hubOffset + len(hub)
    while j < elementsPerSeq:
      seq.append(nextElemIdx)
      nextElemIdx += 1
      j += 1
    sequences.append(seq)
  
  # Write out the sequences in random order
  seqIdxs = []
  for _ in range(numRepeats):
    seqIdxs += range(numSequences)
  random.shuffle(seqIdxs)
  
  for seqIdx in seqIdxs:
    reset = int(resets)
    seq = sequences[seqIdx]
    for (x) in seq:
      outFile.appendRecord([reset, str(x), x])
      reset = 0

  outFile.close()