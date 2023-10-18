def getModelIDFromParamsHash(self, paramsHash):
    """ Return the modelID of the model with the given paramsHash, or
    None if not found.

    Parameters:
    ---------------------------------------------------------------------
    paramsHash:  paramsHash to look for
    retval:      modelId, or None if not found
    """
    entryIdx = self. _paramsHashToIndexes.get(paramsHash, None)
    if entryIdx is not None:
      return self._allResults[entryIdx]['modelID']
    else:
      return None