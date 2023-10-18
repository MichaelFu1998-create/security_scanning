def _createSegment(cls, connections, lastUsedIterationForSegment, cell,
                     iteration, maxSegmentsPerCell):
    """
    Create a segment on the connections, enforcing the maxSegmentsPerCell
    parameter.
    """
    # Enforce maxSegmentsPerCell.
    while connections.numSegments(cell) >= maxSegmentsPerCell:
      leastRecentlyUsedSegment = min(
        connections.segmentsForCell(cell),
        key=lambda segment : lastUsedIterationForSegment[segment.flatIdx])

      connections.destroySegment(leastRecentlyUsedSegment)

    # Create the segment.
    segment = connections.createSegment(cell)

    # Do TM-specific bookkeeping for the segment.
    if segment.flatIdx == len(lastUsedIterationForSegment):
      lastUsedIterationForSegment.append(iteration)
    elif segment.flatIdx < len(lastUsedIterationForSegment):
      # A flatIdx was recycled.
      lastUsedIterationForSegment[segment.flatIdx] = iteration
    else:
      raise AssertionError(
        "All segments should be created with the TM createSegment method.")

    return segment