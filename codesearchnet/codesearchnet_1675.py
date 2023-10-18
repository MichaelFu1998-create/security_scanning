def _addToSegmentUpdates(self, c, i, segUpdate):
    """
    Store a dated potential segment update. The "date" (iteration index) is used
    later to determine whether the update is too old and should be forgotten.
    This is controlled by parameter ``segUpdateValidDuration``.

    :param c: TODO: document
    :param i: TODO: document
    :param segUpdate: TODO: document
    """
    # Sometimes we might be passed an empty update
    if segUpdate is None or len(segUpdate.activeSynapses) == 0:
      return

    key = (c, i) # key = (column index, cell index in column)

    # TODO: scan list of updates for that cell and consolidate?
    # But watch out for dates!
    if self.segmentUpdates.has_key(key):
      self.segmentUpdates[key] += [(self.lrnIterationIdx, segUpdate)]
    else:
      self.segmentUpdates[key] = [(self.lrnIterationIdx, segUpdate)]