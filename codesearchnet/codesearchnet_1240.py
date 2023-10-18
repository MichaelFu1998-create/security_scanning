def _generateFile(filename, numRecords, categoryList, initProb, 
      firstOrderProb, secondOrderProb, seqLen, numNoise=0, resetsEvery=None):
  """ Generate a set of records reflecting a set of probabilities.
  
  Parameters:
  ----------------------------------------------------------------
  filename:         name of .csv file to generate
  numRecords:       number of records to generate
  categoryList:     list of category names
  initProb:         Initial probability for each category. This is a vector
                      of length len(categoryList).
  firstOrderProb:   A dictionary of the 1st order probabilities. The key
                      is the 1st element of the sequence, the value is
                      the probability of each 2nd element given the first. 
  secondOrderProb:  A dictionary of the 2nd order probabilities. The key
                      is the first 2 elements of the sequence, the value is
                      the probability of each possible 3rd element given the 
                      first two. 
  seqLen:           Desired length of each sequence. The 1st element will
                      be generated using the initProb, the 2nd element by the
                      firstOrder table, and the 3rd and all successive 
                      elements by the secondOrder table. None means infinite
                      length. 
  numNoise:         Number of noise elements to place between each 
                      sequence. The noise elements are evenly distributed from 
                      all categories. 
  resetsEvery:      If not None, generate a reset every N records
                      
                      
  Here is an example of some parameters:
  
  categoryList:     ['cat1', 'cat2', 'cat3']
  
  initProb:         [0.7, 0.2, 0.1]
  
  firstOrderProb:   {'[0]': [0.3, 0.3, 0.4],
                     '[1]': [0.3, 0.3, 0.4],
                     '[2]': [0.3, 0.3, 0.4]}
                     
  secondOrderProb:  {'[0,0]': [0.3, 0.3, 0.4],
                     '[0,1]': [0.3, 0.3, 0.4],
                     '[0,2]': [0.3, 0.3, 0.4],
                     '[1,0]': [0.3, 0.3, 0.4],
                     '[1,1]': [0.3, 0.3, 0.4],
                     '[1,2]': [0.3, 0.3, 0.4],
                     '[2,0]': [0.3, 0.3, 0.4],
                     '[2,1]': [0.3, 0.3, 0.4],
                     '[2,2]': [0.3, 0.3, 0.4]}
                   
  """
  
  # Create the file
  print "Creating %s..." % (filename)
  fields = [('reset', 'int', 'R'), ('name', 'string', '')]
  outFile = FileRecordStream(filename, write=True, fields=fields)
  
  # --------------------------------------------------------------------
  # Convert the probabilitie tables into cumulative probabilities
  initCumProb = initProb.cumsum()
  
  firstOrderCumProb = dict()
  for (key,value) in firstOrderProb.iteritems():
    firstOrderCumProb[key] = value.cumsum()
    
  secondOrderCumProb = dict()
  for (key,value) in secondOrderProb.iteritems():
    secondOrderCumProb[key] = value.cumsum()
    

  # --------------------------------------------------------------------
  # Write out the sequences
  elementsInSeq = []
  numElementsSinceReset = 0
  maxCatIdx = len(categoryList) - 1
  for i in xrange(numRecords):

    # Generate a reset?
    if numElementsSinceReset == 0:
      reset = 1
    else:
      reset = 0
      
    # Pick the next element, based on how are we are into the 2nd order
    #   sequence. 
    rand = numpy.random.rand()
    if len(elementsInSeq) == 0:
      catIdx = numpy.searchsorted(initCumProb, rand)
    elif len(elementsInSeq) == 1:
      catIdx = numpy.searchsorted(firstOrderCumProb[str(elementsInSeq)], rand)
    elif (len(elementsInSeq) >=2) and \
                  (seqLen is None or len(elementsInSeq) < seqLen-numNoise):
      catIdx = numpy.searchsorted(secondOrderCumProb[str(elementsInSeq[-2:])], rand)
    else:   # random "noise"
      catIdx = numpy.random.randint(len(categoryList))
      
    # Write out the record
    catIdx = min(maxCatIdx, catIdx)
    outFile.appendRecord([reset,categoryList[catIdx]])    
    #print categoryList[catIdx]
    
    # ------------------------------------------------------------
    # Increment counters
    elementsInSeq.append(catIdx)
    numElementsSinceReset += 1
    
    # Generate another reset?
    if resetsEvery is not None and numElementsSinceReset == resetsEvery:
      numElementsSinceReset = 0
      elementsInSeq = []
    
    # Start another 2nd order sequence?
    if seqLen is not None and (len(elementsInSeq) == seqLen+numNoise):
      elementsInSeq = []
      
  
  outFile.close()