def createSegment(self, cell):
    """ 
    Adds a new segment on a cell.

    :param cell: (int) Cell index
    :returns: (int) New segment index
    """
    cellData = self._cells[cell]

    if len(self._freeFlatIdxs) > 0:
      flatIdx = self._freeFlatIdxs.pop()
    else:
      flatIdx = self._nextFlatIdx
      self._segmentForFlatIdx.append(None)
      self._nextFlatIdx += 1

    ordinal = self._nextSegmentOrdinal
    self._nextSegmentOrdinal += 1

    segment = Segment(cell, flatIdx, ordinal)
    cellData._segments.append(segment)
    self._segmentForFlatIdx[flatIdx] = segment

    return segment