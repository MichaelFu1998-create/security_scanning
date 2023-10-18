def appendInputWithSimilarValues(inputs):
  """ Creates an 'one-off' record for each record in the inputs. Appends new
  records to the same inputs list.
  """
  numInputs = len(inputs)
  for i in xrange(numInputs):
    input = inputs[i]
    for j in xrange(len(input)-1):
      if input[j] == 1 and input[j+1] == 0:
        newInput = copy.deepcopy(input)
        newInput[j] = 0
        newInput[j+1] = 1
        inputs.append(newInput)
        break