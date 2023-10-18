def printOutput(self, y):
    """
    TODO: document
    
    :param y: 
    :return: 
    """
    print "Output"
    for i in xrange(self.cellsPerColumn):
      for c in xrange(self.numberOfCols):
        print int(y[c, i]),
      print