def destroySegment(self, segment):
    """
    Destroys a segment.

    :param segment: (:class:`Segment`) representing the segment to be destroyed.
    """
    # Remove the synapses from all data structures outside this Segment.
    for synapse in segment._synapses:
      self._removeSynapseFromPresynapticMap(synapse)
    self._numSynapses -= len(segment._synapses)

    # Remove the segment from the cell's list.
    segments = self._cells[segment.cell]._segments
    i = segments.index(segment)
    del segments[i]

    # Free the flatIdx and remove the final reference so the Segment can be
    # garbage-collected.
    self._freeFlatIdxs.append(segment.flatIdx)
    self._segmentForFlatIdx[segment.flatIdx] = None