def numModels(self, swarmId=None, includeHidden=False):
    """Return the total # of models we have in our database (if swarmId is
    None) or in a specific swarm.

    Parameters:
    ---------------------------------------------------------------------
    swarmId:        A string representation of the sorted list of encoders
                    in this swarm. For example '__address_encoder.__gym_encoder'
    includeHidden:  If False, this will only return the number of models
                    that are not hidden (i.e. orphanned, etc.)
    retval:  numModels
    """
    # Count all models
    if includeHidden:
      if swarmId is None:
        return len(self._allResults)

      else:
        return len(self._swarmIdToIndexes.get(swarmId, []))
    # Only count non-hidden models
    else:
      if swarmId is None:
        entries = self._allResults
      else:
        entries = [self._allResults[entryIdx]
                   for entryIdx in self._swarmIdToIndexes.get(swarmId,[])]

      return len([entry for entry in entries if not entry['hidden']])