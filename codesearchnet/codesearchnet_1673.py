def printCells(self, predictedOnly=False):
    """
    TODO: document
    
    :param predictedOnly: 
    :return: 
    """
    if predictedOnly:
      print "--- PREDICTED CELLS ---"
    else:
      print "--- ALL CELLS ---"
    print "Activation threshold=", self.activationThreshold,
    print "min threshold=", self.minThreshold,
    print "connected perm=", self.connectedPerm

    for c in xrange(self.numberOfCols):
      for i in xrange(self.cellsPerColumn):
        if not predictedOnly or self.infPredictedState['t'][c, i]:
          self.printCell(c, i, predictedOnly)