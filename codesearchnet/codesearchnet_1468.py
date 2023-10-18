def createSegment(self, cell):
    """
    Create a :class:`~nupic.algorithms.connections.Segment` on the specified 
    cell. This method calls 
    :meth:`~nupic.algorithms.connections.Connections.createSegment` on the 
    underlying :class:`~nupic.algorithms.connections.Connections`, and it does 
    some extra bookkeeping. Unit tests should call this method, and not 
    :meth:`~nupic.algorithms.connections.Connections.createSegment`.

    :param cell: (int) Index of cell to create a segment on.

    :returns: (:class:`~nupic.algorithms.connections.Segment`) The created 
              segment.
    """
    return self._createSegment(
      self.connections, self.lastUsedIterationForSegment, cell, self.iteration,
      self.maxSegmentsPerCell)