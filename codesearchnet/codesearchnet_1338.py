def topDownCompute(self, topDownIn=None):
    """
    (From `backtracking_tm.py`)
    Top-down compute - generate expected input given output of the TM

    @param topDownIn top down input from the level above us

    @returns best estimate of the TM input that would have generated bottomUpOut.
    """
    output = numpy.zeros(self.numberOfColumns())
    columns = [self.columnForCell(idx) for idx in self.getPredictiveCells()]
    output[columns] = 1
    return output