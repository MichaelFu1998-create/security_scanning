def printStates(self, printPrevious = True, printLearnState = True):
    """
    TODO: document
    
    :param printPrevious: 
    :param printLearnState: 
    :return: 
    """
    def formatRow(var, i):
      s = ''
      for c in range(self.numberOfCols):
        if c > 0 and c % 10 == 0:
          s += ' '
        s += str(var[c, i])
      s += ' '
      return s

    print "\nInference Active state"
    for i in xrange(self.cellsPerColumn):
      if printPrevious:
        print formatRow(self.infActiveState['t-1'], i),
      print formatRow(self.infActiveState['t'], i)

    print "Inference Predicted state"
    for i in xrange(self.cellsPerColumn):
      if printPrevious:
        print formatRow(self.infPredictedState['t-1'], i),
      print formatRow(self.infPredictedState['t'], i)

    if printLearnState:
      print "\nLearn Active state"
      for i in xrange(self.cellsPerColumn):
        if printPrevious:
          print formatRow(self.lrnActiveState['t-1'], i),
        print formatRow(self.lrnActiveState['t'], i)

      print "Learn Predicted state"
      for i in xrange(self.cellsPerColumn):
        if printPrevious:
          print formatRow(self.lrnPredictedState['t-1'], i),
        print formatRow(self.lrnPredictedState['t'], i)