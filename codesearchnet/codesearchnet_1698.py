def _getCellForNewSegment(self, colIdx):
    """
    Return the index of a cell in this column which is a good candidate
    for adding a new segment.

    When we have fixed size resources in effect, we insure that we pick a
    cell which does not already have the max number of allowed segments. If
    none exists, we choose the least used segment in the column to re-allocate.

    :param colIdx which column to look at
    :returns: cell index
    """
    # Not fixed size CLA, just choose a cell randomly
    if self.maxSegmentsPerCell < 0:
      if self.cellsPerColumn > 1:
        # Don't ever choose the start cell (cell # 0) in each column
        i = self._random.getUInt32(self.cellsPerColumn-1) + 1
      else:
        i = 0
      return i

    # Fixed size CLA, choose from among the cells that are below the maximum
    # number of segments.
    # NOTE: It is important NOT to always pick the cell with the fewest number
    # of segments. The reason is that if we always do that, we are more likely
    # to run into situations where we choose the same set of cell indices to
    # represent an 'A' in both context 1 and context 2. This is because the
    # cell indices we choose in each column of a pattern will advance in
    # lockstep (i.e. we pick cell indices of 1, then cell indices of 2, etc.).
    candidateCellIdxs = []
    if self.cellsPerColumn == 1:
      minIdx = 0
      maxIdx = 0
    else:
      minIdx = 1                      # Don't include startCell in the mix
      maxIdx = self.cellsPerColumn-1
    for i in xrange(minIdx, maxIdx+1):
      numSegs = len(self.cells[colIdx][i])
      if numSegs < self.maxSegmentsPerCell:
        candidateCellIdxs.append(i)

    # If we found one, return with it. Note we need to use _random to maintain
    # correspondence with CPP code.
    if len(candidateCellIdxs) > 0:
      #candidateCellIdx = random.choice(candidateCellIdxs)
      candidateCellIdx = (
          candidateCellIdxs[self._random.getUInt32(len(candidateCellIdxs))])
      if self.verbosity >= 5:
        print "Cell [%d,%d] chosen for new segment, # of segs is %d" % (
            colIdx, candidateCellIdx, len(self.cells[colIdx][candidateCellIdx]))
      return candidateCellIdx

    # All cells in the column are full, find a segment to free up
    candidateSegment = None
    candidateSegmentDC = 1.0
    # For each cell in this column
    for i in xrange(minIdx, maxIdx+1):
      # For each segment in this cell
      for s in self.cells[colIdx][i]:
        dc = s.dutyCycle()
        if dc < candidateSegmentDC:
          candidateCellIdx = i
          candidateSegmentDC = dc
          candidateSegment = s

    # Free up the least used segment
    if self.verbosity >= 5:
      print ("Deleting segment #%d for cell[%d,%d] to make room for new "
             "segment" % (candidateSegment.segID, colIdx, candidateCellIdx))
      candidateSegment.debugPrint()
    self._cleanUpdatesList(colIdx, candidateCellIdx, candidateSegment)
    self.cells[colIdx][candidateCellIdx].remove(candidateSegment)
    return candidateCellIdx