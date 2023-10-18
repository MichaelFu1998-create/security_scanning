def _inferPhase1(self, activeColumns, useStartCells):
    """
    Update the inference active state from the last set of predictions
    and the current bottom-up.

    This looks at:
        - ``infPredictedState['t-1']``
    This modifies:
        - ``infActiveState['t']``

    :param activeColumns: (list) active bottom-ups
    :param useStartCells: (bool) If true, ignore previous predictions and simply 
           turn on the start cells in the active columns
    :returns: (bool) True if the current input was sufficiently predicted, OR if 
           we started over on startCells. False indicates that the current input 
           was NOT predicted, and we are now bursting on most columns.
    """
    # Init to zeros to start
    self.infActiveState['t'].fill(0)

    # Phase 1 - turn on predicted cells in each column receiving bottom-up
    # If we are following a reset, activate only the start cell in each
    # column that has bottom-up
    numPredictedColumns = 0
    if useStartCells:
      for c in activeColumns:
        self.infActiveState['t'][c, 0] = 1

    # else, turn on any predicted cells in each column. If there are none, then
    # turn on all cells (burst the column)
    else:
      for c in activeColumns:
        predictingCells = numpy.where(self.infPredictedState['t-1'][c] == 1)[0]
        numPredictingCells = len(predictingCells)

        if numPredictingCells > 0:
          self.infActiveState['t'][c, predictingCells] = 1
          numPredictedColumns += 1

        else:
          self.infActiveState['t'][c, :] = 1 # whole column bursts

    # Did we predict this input well enough?
    if useStartCells or numPredictedColumns >= 0.50 * len(activeColumns):
      return True
    else:
      return False