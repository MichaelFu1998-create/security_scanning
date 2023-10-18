def _cleanUpdatesList(self, col, cellIdx, seg):
    """
    Removes any update that would be for the given col, cellIdx, segIdx.

    NOTE: logically, we need to do this when we delete segments, so that if
    an update refers to a segment that was just deleted, we also remove
    that update from the update list. However, I haven't seen it trigger
    in any of the unit tests yet, so it might mean that it's not needed
    and that situation doesn't occur, by construction.
    """
    # TODO: check if the situation described in the docstring above actually
    #       occurs.
    for key, updateList in self.segmentUpdates.iteritems():
      c, i = key[0], key[1]
      if c == col and i == cellIdx:
        for update in updateList:
          if update[1].segment == seg:
            self._removeSegmentUpdate(update)