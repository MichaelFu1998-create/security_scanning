def _generateSimple(filename="simple.csv", numSequences=1, elementsPerSeq=3, 
                    numRepeats=10):
  """ Generate a simple dataset. This contains a bunch of non-overlapping
  sequences. 
  
  At the end of the dataset, we introduce missing records so that test
  code can insure that the model didn't get confused by them. 
  
  Parameters:
  ----------------------------------------------------
  filename:       name of the file to produce, including extension. It will
                  be created in a 'datasets' sub-directory within the 
                  directory containing this script. 
  numSequences:   how many sequences to generate
  elementsPerSeq: length of each sequence
  numRepeats:     how many times to repeat each sequence in the output 
  """
  
  # Create the output file
  scriptDir = os.path.dirname(__file__)
  pathname = os.path.join(scriptDir, 'datasets', filename)
  print "Creating %s..." % (pathname)
  fields = [('timestamp', 'datetime', 'T'), 
            ('field1', 'string', ''),  
            ('field2', 'float', '')]  
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
  
  # Put 1 hour between each record
  timestamp = datetime.datetime(year=2012, month=1, day=1, hour=0, minute=0,
                                second=0)
  timeDelta = datetime.timedelta(hours=1)
  
  # Write out the sequences without missing records
  for seqIdx in seqIdxs:
    seq = sequences[seqIdx]
    for x in seq:
      outFile.appendRecord([timestamp, str(x), x])
      timestamp += timeDelta
      
  # Now, write some out with missing records
  for seqIdx in seqIdxs:
    seq = sequences[seqIdx]
    for i,x in enumerate(seq):
      if i != 1:
        outFile.appendRecord([timestamp, str(x), x])
      timestamp += timeDelta
  for seqIdx in seqIdxs:
    seq = sequences[seqIdx]
    for i,x in enumerate(seq):
      if i != 1:
        outFile.appendRecord([timestamp, str(x), x])
      timestamp += timeDelta

  # Write out some more of the sequences *without* missing records
  for seqIdx in seqIdxs:
    seq = sequences[seqIdx]
    for x in seq:
      outFile.appendRecord([timestamp, str(x), x])
      timestamp += timeDelta
      
  

  outFile.close()