def _computeOutput(self):
    """
    Computes output for both learning and inference. In both cases, the
    output is the boolean OR of ``activeState`` and ``predictedState`` at ``t``.
    Stores ``currentOutput`` for ``checkPrediction``.
    
    :returns: TODO: document
    """
    # TODO: This operation can be sped up by:
    #  1.)  Pre-allocating space for the currentOutput
    #  2.)  Making predictedState and activeState of type 'float32' up front
    #  3.)  Using logical_or(self.predictedState['t'], self.activeState['t'],
    #          self.currentOutput)

    if self.outputType == 'activeState1CellPerCol':

      # Fire only the most confident cell in columns that have 2 or more
      #  active cells
      mostActiveCellPerCol = self.cellConfidence['t'].argmax(axis=1)
      self.currentOutput = numpy.zeros(self.infActiveState['t'].shape,
                                       dtype='float32')

      # Turn on the most confident cell in each column. Note here that
      #  Columns refers to TM columns, even though each TM column is a row
      #  in the numpy array.
      numCols = self.currentOutput.shape[0]
      self.currentOutput[(xrange(numCols), mostActiveCellPerCol)] = 1

      # Don't turn on anything in columns which are not active at all
      activeCols = self.infActiveState['t'].max(axis=1)
      inactiveCols = numpy.where(activeCols==0)[0]
      self.currentOutput[inactiveCols, :] = 0


    elif self.outputType == 'activeState':
      self.currentOutput = self.infActiveState['t']

    elif self.outputType == 'normal':
      self.currentOutput = numpy.logical_or(self.infPredictedState['t'],
                                            self.infActiveState['t'])

    else:
      raise RuntimeError("Unimplemented outputType")

    return self.currentOutput.reshape(-1).astype('float32')