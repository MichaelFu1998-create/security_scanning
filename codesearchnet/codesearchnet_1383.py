def analyzeOverlaps(activeCoincsFile, encodingsFile, dataset):
  '''Mirror Image Visualization: Shows the encoding space juxtaposed against the
  coincidence space. The encoding space is the bottom-up sensory encoding and
  the coincidence space depicts the corresponding activation of coincidences in
  the SP. Hence, the mirror image visualization is a visual depiction of the
  mapping of SP cells to the input representations.
  
  Note:
  * The files spBUOut and sensorBUOut are assumed to be in the output format
  used for LPF experiment outputs.
  * BU outputs for some sample datasets are provided. Specify the name of the
  dataset as an option while running this script. 
  '''
  
  lines = activeCoincsFile.readlines()
  inputs = encodingsFile.readlines()
  w = len(inputs[0].split(' '))-1

  patterns = set([])
  encodings = set([])
  coincs = []    #The set of all coincidences that have won at least once
  reUsedCoincs = []
  
  firstLine = inputs[0].split(' ')
  size = int(firstLine.pop(0))
  spOutput = np.zeros((len(lines),40))
  inputBits = np.zeros((len(lines),w))
  print 'Total n:', size
  print 'Total number of records in the file:', len(lines), '\n'
  print 'w:', w
  
  count = 0
  for x in xrange(len(lines)):
    inputSpace = []     #Encoded representation for each input 
    
    spBUout = [int(z) for z in lines[x].split(' ')]  
    spBUout.pop(0)         #The first element of each row of spBUOut is the size of the SP 
    temp = set(spBUout)
    spOutput[x]=spBUout
    
    input = [int(z) for z in inputs[x].split(' ')]    
    input.pop(0)   #The first element of each row of sensorBUout is the size of the encoding space
    tempInput = set(input)
    inputBits[x]=input
    
    #Creating the encoding space 
    for m in xrange(size):
      if m in tempInput:
        inputSpace.append(m)
      else:
        inputSpace.append('|')  #A non-active bit
    
    repeatedBits = tempInput.intersection(encodings)    #Storing the bits that have been previously active
    reUsed = temp.intersection(patterns)  #Checking if any of the active cells have been previously active  
    
    #Dividing the coincidences into two difference categories. 
    if len(reUsed)==0:
      coincs.append((count,temp,repeatedBits,inputSpace, tempInput))  #Pattern no, active cells, repeated bits, encoding (full), encoding (summary)
    else:
      reUsedCoincs.append((count,temp,repeatedBits,inputSpace, tempInput))
    patterns=patterns.union(temp)   #Adding the active cells to the set of coincs that have been active at least once
    
    encodings = encodings.union(tempInput)
    count +=1
    
  overlap = {}
  overlapVal = 0

  seen = []
  seen = (printOverlaps(coincs, coincs, seen))
  print len(seen), 'sets of 40 cells'
  seen = printOverlaps(reUsedCoincs, coincs, seen)
  
  Summ=[]
  for z in coincs:
    c=0
    for y in reUsedCoincs:
      c += len(z[1].intersection(y[1]))
    Summ.append(c)
  print 'Sum: ', Summ
  
  for m in xrange(3):
    displayLimit = min(51, len(spOutput[m*200:]))
    if displayLimit>0:
      drawFile(dataset, np.zeros([len(inputBits[:(m+1)*displayLimit]),len(inputBits[:(m+1)*displayLimit])]), inputBits[:(m+1)*displayLimit], spOutput[:(m+1)*displayLimit], w, m+1)
    else: 
      print 'No more records to display'
  pyl.show()