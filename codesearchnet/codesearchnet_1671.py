def printComputeEnd(self, output, learn=False):
    """
    Called at the end of inference to print out various diagnostic
    information based on the current verbosity level.

    :param output: TODO: document
    :param learn: TODO: document
    """
    if self.verbosity >= 3:
      print "----- computeEnd summary: "
      print "learn:", learn
      print "numBurstingCols: %s, " % (
          self.infActiveState['t'].min(axis=1).sum()),
      print "curPredScore2: %s, " % (
          self._internalStats['curPredictionScore2']),
      print "curFalsePosScore: %s, " % (
          self._internalStats['curFalsePositiveScore']),
      print "1-curFalseNegScore: %s, " % (
          1 - self._internalStats['curFalseNegativeScore'])
      print "numSegments: ", self.getNumSegments(),
      print "avgLearnedSeqLength: ", self.avgLearnedSeqLength

      print "----- infActiveState (%d on) ------" % (
          self.infActiveState['t'].sum())
      self.printActiveIndices(self.infActiveState['t'])
      if self.verbosity >= 6:
        self.printState(self.infActiveState['t'])

      print "----- infPredictedState (%d on)-----" % (
          self.infPredictedState['t'].sum())
      self.printActiveIndices(self.infPredictedState['t'])
      if self.verbosity >= 6:
        self.printState(self.infPredictedState['t'])

      print "----- lrnActiveState (%d on) ------" % (
          self.lrnActiveState['t'].sum())
      self.printActiveIndices(self.lrnActiveState['t'])
      if self.verbosity >= 6:
        self.printState(self.lrnActiveState['t'])

      print "----- lrnPredictedState (%d on)-----" % (
          self.lrnPredictedState['t'].sum())
      self.printActiveIndices(self.lrnPredictedState['t'])
      if self.verbosity >= 6:
        self.printState(self.lrnPredictedState['t'])


      print "----- cellConfidence -----"
      self.printActiveIndices(self.cellConfidence['t'], andValues=True)
      if self.verbosity >= 6:
        self.printConfidence(self.cellConfidence['t'])

      print "----- colConfidence -----"
      self.printActiveIndices(self.colConfidence['t'], andValues=True)

      print "----- cellConfidence[t-1] for currently active cells -----"
      cc = self.cellConfidence['t-1'] * self.infActiveState['t']
      self.printActiveIndices(cc, andValues=True)

      if self.verbosity == 4:
        print "Cells, predicted segments only:"
        self.printCells(predictedOnly=True)
      elif self.verbosity >= 5:
        print "Cells, all segments:"
        self.printCells(predictedOnly=False)
      print

    elif self.verbosity >= 1:
      print "TM: learn:", learn
      print "TM: active outputs(%d):" % len(output.nonzero()[0]),
      self.printActiveIndices(output.reshape(self.numberOfCols,
                                             self.cellsPerColumn))