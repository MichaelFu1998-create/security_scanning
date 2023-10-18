def trainTM(sequence, timeSteps, noiseLevel):
  """
  Trains the TM with given sequence for a given number of time steps and level of input
  corruption
  
  @param sequence   (array) array whose rows are the input characters
  @param timeSteps  (int)   number of time steps in which the TM will be presented with sequence
  @param noiseLevel (float) amount of noise to be applied on the characters in the sequence 
  """
  currentColumns = np.zeros(tm.numberOfColumns(), dtype="uint32")
  predictedColumns = np.zeros(tm.numberOfColumns(), dtype="uint32")
  ts = 0  
  for t in range(timeSteps):
    tm.reset()
    for k in range(4):
      v = corruptVector(sequence[k][:], noiseLevel, sparseCols)
      tm.compute(set(v[:].nonzero()[0].tolist()), learn=True)
      activeColumnsIndices = [tm.columnForCell(i) for i in tm.getActiveCells()]
      predictedColumnIndices = [tm.columnForCell(i) for i in tm.getPredictiveCells()]
      currentColumns = [1 if i in activeColumnsIndices else 0 for i in range(tm.numberOfColumns())]
      acc = accuracy(currentColumns, predictedColumns)
      x.append(ts)
      y.append(acc)
      ts += 1
      predictedColumns = [1 if i in predictedColumnIndices else 0 for i in range(tm.numberOfColumns())]