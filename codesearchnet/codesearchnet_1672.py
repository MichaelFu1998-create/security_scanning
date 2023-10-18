def printCell(self, c, i, onlyActiveSegments=False):
    """
    TODO: document
    
    :param c: 
    :param i: 
    :param onlyActiveSegments: 
    :return: 
    """

    if len(self.cells[c][i]) > 0:
      print "Column", c, "Cell", i, ":",
      print len(self.cells[c][i]), "segment(s)"
      for j, s in enumerate(self.cells[c][i]):
        isActive = self._isSegmentActive(s, self.infActiveState['t'])
        if not onlyActiveSegments or isActive:
          isActiveStr = "*" if isActive else " "
          print "  %sSeg #%-3d" % (isActiveStr, j),
          s.debugPrint()