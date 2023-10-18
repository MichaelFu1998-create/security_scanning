def checkMatch(input, prediction, sparse=True, verbosity=0):
  """
  Compares the actual input with the predicted input and returns results

  Parameters:
  -----------------------------------------------
  input:          The actual input
  prediction:     the predicted input
  verbosity:        If > 0, print debugging messages
  sparse:         If true, they are in sparse form (list of
                     active indices)

  retval         (foundInInput, totalActiveInInput, missingFromInput,
                            totalActiveInPrediction)
    foundInInput:       The number of predicted active elements that were
                        found in the actual input
    totalActiveInInput: The total number of active elements in the input.
    missingFromInput:   The number of predicted active elements that were not
                        found in the actual input
    totalActiveInPrediction:  The total number of active elements in the prediction

  """

  if sparse:
    activeElementsInInput = set(input)
    activeElementsInPrediction = set(prediction)

  else:
    activeElementsInInput = set(input.nonzero()[0])
    activeElementsInPrediction = set(prediction.nonzero()[0])

  totalActiveInPrediction = len(activeElementsInPrediction)
  totalActiveInInput     = len(activeElementsInInput)

  foundInInput = len(activeElementsInPrediction.intersection(activeElementsInInput))
  missingFromInput = len(activeElementsInPrediction.difference(activeElementsInInput))
  missingFromPrediction = len(activeElementsInInput.difference(activeElementsInPrediction))

  if verbosity >= 1:
    print "preds. found in input:", foundInInput, "out of", totalActiveInPrediction,
    print "; preds. missing from input:", missingFromInput, "out of", \
              totalActiveInPrediction,
    print "; unexpected active in input:", missingFromPrediction, "out of", \
              totalActiveInInput

  return (foundInInput, totalActiveInInput, missingFromInput,
          totalActiveInPrediction)