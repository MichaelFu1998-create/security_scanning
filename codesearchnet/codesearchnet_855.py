def __deleteOutputCache(self, modelID):
    """
    Delete's the output cache associated with the given modelID. This actually
    clears up the resources associated with the cache, rather than deleting al
    the records in the cache

    Parameters:
    -----------------------------------------------------------------------
    modelID:      The id of the model whose output cache is being deleted

    """

    # If this is our output, we should close the connection
    if modelID == self._modelID and self._predictionLogger is not None:
      self._predictionLogger.close()
      del self.__predictionCache
      self._predictionLogger = None
      self.__predictionCache = None