def appendInputWithNSimilarValues(inputs, numNear = 10):
  """ Creates a neighboring record for each record in the inputs and adds
  new records at the end of the inputs list
  """
  numInputs = len(inputs)
  skipOne = False
  for i in xrange(numInputs):
    input = inputs[i]
    numChanged = 0
    newInput = copy.deepcopy(input)
    for j in xrange(len(input)-1):
      if skipOne:
        skipOne = False
        continue
      if input[j] == 1 and input[j+1] == 0:
        newInput[j] = 0
        newInput[j+1] = 1
        inputs.append(newInput)
        newInput = copy.deepcopy(newInput)
        #print input
        #print newInput
        numChanged += 1
        skipOne = True
        if numChanged == numNear:
          break