def showPredictions():
  """
  Shows predictions of the TM when presented with the characters A, B, C, D, X, and
  Y without any contextual information, that is, not embedded within a sequence.
  """   
  for k in range(6):
    tm.reset()
    print "--- " + "ABCDXY"[k] + " ---"
    tm.compute(set(seqT[k][:].nonzero()[0].tolist()), learn=False)
    activeColumnsIndices = [tm.columnForCell(i) for i in tm.getActiveCells()]
    predictedColumnIndices = [tm.columnForCell(i) for i in tm.getPredictiveCells()]  
    currentColumns = [1 if i in activeColumnsIndices else 0 for i in range(tm.numberOfColumns())]
    predictedColumns = [1 if i in predictedColumnIndices else 0 for i in range(tm.numberOfColumns())]
    print("Active cols: " + str(np.nonzero(currentColumns)[0]))
    print("Predicted cols: " + str(np.nonzero(predictedColumns)[0]))
    print ""