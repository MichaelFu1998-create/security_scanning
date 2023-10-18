def _constructClassificationRecord(self, inputs):
    """
    Construct a _HTMClassificationRecord based on the state of the model
    passed in through the inputs.

    Types for self.classificationVectorType:
      1 - TM active cells in learn state
      2 - SP columns concatenated with error from TM column predictions and SP
    """
    # Count the number of unpredicted columns
    allSPColumns = inputs["spBottomUpOut"]
    activeSPColumns = allSPColumns.nonzero()[0]

    score = anomaly.computeRawAnomalyScore(activeSPColumns,
                                           self._prevPredictedColumns)

    spSize = len(allSPColumns)


    allTPCells = inputs['tpTopDownOut']
    tpSize = len(inputs['tpLrnActiveStateT'])

    classificationVector = numpy.array([])

    if self.classificationVectorType == 1:
      # Classification Vector: [---TM Cells---]
      classificationVector = numpy.zeros(tpSize)
      activeCellMatrix = inputs["tpLrnActiveStateT"].reshape(tpSize, 1)
      activeCellIdx = numpy.where(activeCellMatrix > 0)[0]
      if activeCellIdx.shape[0] > 0:
        classificationVector[numpy.array(activeCellIdx, dtype=numpy.uint16)] = 1
    elif self.classificationVectorType == 2:
      # Classification Vecotr: [---SP---|---(TM-SP)----]
      classificationVector = numpy.zeros(spSize+spSize)
      if activeSPColumns.shape[0] > 0:
        classificationVector[activeSPColumns] = 1.0

      errorColumns = numpy.setdiff1d(self._prevPredictedColumns,
          activeSPColumns)
      if errorColumns.shape[0] > 0:
        errorColumnIndexes = ( numpy.array(errorColumns, dtype=numpy.uint16) +
          spSize )
        classificationVector[errorColumnIndexes] = 1.0
    else:
      raise TypeError("Classification vector type must be either 'tpc' or"
        " 'sp_tpe', current value is %s" % (self.classificationVectorType))

    # Store the state for next time step
    numPredictedCols = len(self._prevPredictedColumns)
    predictedColumns = allTPCells.nonzero()[0]
    self._prevPredictedColumns = copy.deepcopy(predictedColumns)

    if self._anomalyVectorLength is None:
      self._anomalyVectorLength = len(classificationVector)

    result = _CLAClassificationRecord(
      ROWID=self._iteration, #__numRunCalls called
        #at beginning of model.run
      anomalyScore=score,
      anomalyVector=classificationVector.nonzero()[0].tolist(),
      anomalyLabel=[]
    )
    return result