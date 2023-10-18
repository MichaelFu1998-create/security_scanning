def _generateCategory(filename="simple.csv", numSequences=2, elementsPerSeq=1, 
                    numRepeats=10, resets=False):
  """ Generate a simple dataset. This contains a bunch of non-overlapping
  sequences. 
  
  Parameters:
  ----------------------------------------------------
  filename:       name of the file to produce, including extension. It will
                  be created in a 'datasets' sub-directory within the 
                  directory containing this script. 
  numSequences:   how many sequences to generate
  elementsPerSeq: length of each sequence
  numRepeats:     how many times to repeat each sequence in the output 
  resets:         if True, turn on reset at start of each sequence
  """
  
  # Create the output file
  scriptDir = os.path.dirname(__file__)
  pathname = os.path.join(scriptDir, 'datasets', filename)
  print "Creating %s..." % (pathname)
  fields = [('reset', 'int', 'R'), ('category', 'int', 'C'),
            ('field1', 'string', '')]  
  outFile = FileRecordStream(pathname, write=True, fields=fields)
  
  # Create the sequences
  sequences = []
  for i in range(numSequences):
    seq = [x for x in range(i*elementsPerSeq, (i+1)*elementsPerSeq)]
    sequences.append(seq)
  
  # Write out the sequences in random order
  seqIdxs = []
  for i in range(numRepeats):
    seqIdxs += range(numSequences)
  random.shuffle(seqIdxs)
  
  for seqIdx in seqIdxs:
    reset = int(resets)
    seq = sequences[seqIdx]
    for x in seq:
      outFile.appendRecord([reset, str(seqIdx), str(x)])
      reset = 0

  outFile.close()