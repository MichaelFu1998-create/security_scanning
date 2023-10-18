def segmentPositionSortKey(self, segment):
    """ 
    Return a numeric key for sorting this segment. This can be used with the 
    python built-in ``sorted()`` function.

    :param segment: (:class:`Segment`) within this :class:`Connections` 
           instance.
    :returns: (float) A numeric key for sorting.
    """
    return segment.cell + (segment._ordinal / float(self._nextSegmentOrdinal))