def getSegmentOnCell(self, c, i, segIdx):
    """
    :param c: (int) column index
    :param i: (int) cell index in column
    :param segIdx: (int) segment index to match

    :returns: (list) representing the the segment on cell (c, i) with index 
        ``segIdx``.
        ::

          [  [segmentID, sequenceSegmentFlag, positiveActivations,
              totalActivations, lastActiveIteration,
              lastPosDutyCycle, lastPosDutyCycleIteration],
             [col1, idx1, perm1],
             [col2, idx2, perm2], ...
          ]

    """
    seg = self.cells[c][i][segIdx]
    retlist = [[seg.segID, seg.isSequenceSeg, seg.positiveActivations,
                seg.totalActivations, seg.lastActiveIteration,
                seg._lastPosDutyCycle, seg._lastPosDutyCycleIteration]]
    retlist += seg.syns
    return retlist