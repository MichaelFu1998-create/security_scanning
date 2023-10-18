def _trimSegmentsInCell(self, colIdx, cellIdx, segList, minPermanence,
                          minNumSyns):
    """
    This method goes through a list of segments for a given cell and
    deletes all synapses whose permanence is less than minPermanence and deletes
    any segments that have less than minNumSyns synapses remaining.

    :param colIdx        Column index
    :param cellIdx       Cell index within the column
    :param segList       List of segment references
    :param minPermanence Any syn whose permamence is 0 or < minPermanence will
                         be deleted.
    :param minNumSyns    Any segment with less than minNumSyns synapses remaining
                         in it will be deleted.

    :returns: tuple (numSegsRemoved, numSynsRemoved)
    """
    # Fill in defaults
    if minPermanence is None:
      minPermanence = self.connectedPerm
    if minNumSyns is None:
      minNumSyns = self.activationThreshold

    # Loop through all segments
    nSegsRemoved, nSynsRemoved = 0, 0
    segsToDel = [] # collect and remove segments outside the loop
    for segment in segList:

      # List if synapses to delete
      synsToDel = [syn for syn in segment.syns if syn[2] < minPermanence]

      if len(synsToDel) == len(segment.syns):
        segsToDel.append(segment) # will remove the whole segment
      else:
        if len(synsToDel) > 0:
          for syn in synsToDel: # remove some synapses on segment
            segment.syns.remove(syn)
            nSynsRemoved += 1
        if len(segment.syns) < minNumSyns:
          segsToDel.append(segment)

    # Remove segments that don't have enough synapses and also take them
    # out of the segment update list, if they are in there
    nSegsRemoved += len(segsToDel)
    for seg in segsToDel: # remove some segments of this cell
      self._cleanUpdatesList(colIdx, cellIdx, seg)
      self.cells[colIdx][cellIdx].remove(seg)
      nSynsRemoved += len(seg.syns)

    return nSegsRemoved, nSynsRemoved