def _constructClassificationRecord(self):
    """
    Construct a _HTMClassificationRecord based on the current state of the
    htm_prediction_model of this classifier.

    ***This will look into the internals of the model and may depend on the
    SP, TM, and KNNClassifier***
    """
    model = self.htm_prediction_model
    sp = model._getSPRegion()
    tm = model._getTPRegion()
    tpImp = tm.getSelf()._tfdr

    # Count the number of unpredicted columns
    activeColumns = sp.getOutputData("bottomUpOut").nonzero()[0]
    score = numpy.in1d(activeColumns, self._prevPredictedColumns).sum()
    score = (self._activeColumnCount - score)/float(self._activeColumnCount)

    spSize = sp.getParameter('activeOutputCount')
    tpSize = tm.getParameter('cellsPerColumn') * tm.getParameter('columnCount')

    classificationVector = numpy.array([])

    if self._vectorType == 'tpc':
      # Classification Vector: [---TM Cells---]
      classificationVector = numpy.zeros(tpSize)
      activeCellMatrix = tpImp.getLearnActiveStateT().reshape(tpSize, 1)
      activeCellIdx = numpy.where(activeCellMatrix > 0)[0]
      if activeCellIdx.shape[0] > 0:
        classificationVector[numpy.array(activeCellIdx, dtype=numpy.uint16)] = 1
    elif self._vectorType == 'sp_tpe':
      # Classification Vecotr: [---SP---|---(TM-SP)----]
      classificationVector = numpy.zeros(spSize+spSize)
      if activeColumns.shape[0] > 0:
        classificationVector[activeColumns] = 1.0

      errorColumns = numpy.setdiff1d(self._prevPredictedColumns, activeColumns)
      if errorColumns.shape[0] > 0:
        errorColumnIndexes = ( numpy.array(errorColumns, dtype=numpy.uint16) +
          spSize )
        classificationVector[errorColumnIndexes] = 1.0
    else:
      raise TypeError("Classification vector type must be either 'tpc' or"
        " 'sp_tpe', current value is %s" % (self._vectorType))

    # Store the state for next time step
    numPredictedCols = len(self._prevPredictedColumns)
    predictedColumns = tm.getOutputData("topDownOut").nonzero()[0]
    self._prevPredictedColumns = copy.deepcopy(predictedColumns)

    if self._anomalyVectorLength is None:
      self._anomalyVectorLength = len(classificationVector)

    result = _CLAClassificationRecord(
      ROWID=int(model.getParameter('__numRunCalls') - 1), #__numRunCalls called
        #at beginning of model.run
      anomalyScore=score,
      anomalyVector=classificationVector.nonzero()[0].tolist(),
      anomalyLabel=[]
    )
    return result