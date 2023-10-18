def _processSegmentUpdates(self, activeColumns):
    """
    Go through the list of accumulated segment updates and process them
    as follows:

    if the segment update is too old, remove the update
    else if the cell received bottom-up, update its permanences
    else if it's still being predicted, leave it in the queue
    else remove it.

    :param activeColumns TODO: document
    """
    # The segmentUpdates dict has keys which are the column,cellIdx of the
    # owner cell. The values are lists of segment updates for that cell
    removeKeys = []
    trimSegments = []
    for key, updateList in self.segmentUpdates.iteritems():

      # Get the column number and cell index of the owner cell
      c, i = key[0], key[1]

      # If the cell received bottom-up, update its segments
      if c in activeColumns:
        action = 'update'

      # If not, either keep it around if it's still predicted, or remove it
      else:
        # If it is still predicted, and we are pooling, keep it around
        if self.doPooling and self.lrnPredictedState['t'][c, i] == 1:
          action = 'keep'
        else:
          action = 'remove'

      # Process each segment for this cell. Each segment entry contains
      # [creationDate, SegmentInfo]
      updateListKeep = []
      if action != 'remove':
        for (createDate, segUpdate) in updateList:

          if self.verbosity >= 4:
            print "_nLrnIterations =", self.lrnIterationIdx,
            print segUpdate

          # If this segment has expired. Ignore this update (and hence remove it
          # from list)
          if self.lrnIterationIdx - createDate > self.segUpdateValidDuration:
            continue

          if action == 'update':
            trimSegment = self._adaptSegment(segUpdate)
            if trimSegment:
              trimSegments.append((segUpdate.columnIdx, segUpdate.cellIdx,
                                        segUpdate.segment))
          else:
            # Keep segments that haven't expired yet (the cell is still being
            #   predicted)
            updateListKeep.append((createDate, segUpdate))

      self.segmentUpdates[key] = updateListKeep
      if len(updateListKeep) == 0:
        removeKeys.append(key)

    # Clean out empty segment updates
    for key in removeKeys:
      self.segmentUpdates.pop(key)

    # Trim segments that had synapses go to 0
    for (c, i, segment) in trimSegments:
      self._trimSegmentsInCell(c, i, [segment], minPermanence = 0.00001,
                               minNumSyns = 0)