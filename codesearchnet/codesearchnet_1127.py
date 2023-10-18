def _iterModels(modelIDs):
  """Creates an iterator that returns ModelInfo elements for the given modelIDs

  WARNING:      The order of ModelInfo elements returned by the iterator
                may not match the order of the given modelIDs

  Parameters:
  ----------------------------------------------------------------------
  modelIDs:       A sequence of model identifiers (e.g., as returned by
                  _HyperSearchJob.queryModelIDs()).
  retval:         Iterator that returns ModelInfo elements for the given
                  modelIDs (NOTE:possibly in a different order)
  """

  class ModelInfoIterator(object):
    """ModelInfo iterator implementation class
    """

    # Maximum number of ModelInfo elements to load into cache whenever
    # cache empties
    __CACHE_LIMIT = 1000

    debug=False


    def __init__(self, modelIDs):
      """
      Parameters:
      ----------------------------------------------------------------------
      modelIDs:     a sequence of Nupic model identifiers for which this
                    iterator will return _NupicModelInfo instances.
                    NOTE: The returned instances are NOT guaranteed to be in
                    the same order as the IDs in modelIDs sequence.
      retval:       nothing
      """
      # Make our own copy in case caller changes model id list during iteration
      self.__modelIDs = tuple(modelIDs)

      if self.debug:
        _emit(Verbosity.DEBUG,
              "MODELITERATOR: __init__; numModelIDs=%s" % len(self.__modelIDs))

      self.__nextIndex = 0
      self.__modelCache = collections.deque()
      return


    def __iter__(self):
      """Iterator Protocol function

      Parameters:
      ----------------------------------------------------------------------
      retval:         self
      """
      return self



    def next(self):
      """Iterator Protocol function

      Parameters:
      ----------------------------------------------------------------------
      retval:       A _NupicModelInfo instance or raises StopIteration to
                    signal end of iteration.
      """
      return self.__getNext()



    def __getNext(self):
      """Implementation of the next() Iterator Protocol function.

      When the modelInfo cache becomes empty, queries Nupic and fills the cache
      with the next set of NupicModelInfo instances.

      Parameters:
      ----------------------------------------------------------------------
      retval:       A _NupicModelInfo instance or raises StopIteration to
                    signal end of iteration.
      """

      if self.debug:
        _emit(Verbosity.DEBUG,
              "MODELITERATOR: __getNext(); modelCacheLen=%s" % (
                  len(self.__modelCache)))

      if not self.__modelCache:
        self.__fillCache()

      if not self.__modelCache:
        raise StopIteration()

      return self.__modelCache.popleft()



    def __fillCache(self):
      """Queries Nupic and fills an empty modelInfo cache with the next set of
      _NupicModelInfo instances

      Parameters:
      ----------------------------------------------------------------------
      retval:       nothing
      """
      assert (not self.__modelCache)

      # Assemble a list of model IDs to look up
      numModelIDs = len(self.__modelIDs) if self.__modelIDs else 0

      if self.__nextIndex >= numModelIDs:
        return

      idRange = self.__nextIndex + self.__CACHE_LIMIT
      if idRange > numModelIDs:
        idRange = numModelIDs

      lookupIDs = self.__modelIDs[self.__nextIndex:idRange]

      self.__nextIndex += (idRange - self.__nextIndex)

      # Query Nupic for model info of all models in the look-up list
      # NOTE: the order of results may not be the same as lookupIDs
      infoList = _clientJobsDB().modelsInfo(lookupIDs)
      assert len(infoList) == len(lookupIDs), \
            "modelsInfo returned %s elements; expected %s." % \
            (len(infoList), len(lookupIDs))

      # Create _NupicModelInfo instances and add them to cache
      for rawInfo in infoList:
        modelInfo = _NupicModelInfo(rawInfo=rawInfo)
        self.__modelCache.append(modelInfo)

      assert len(self.__modelCache) == len(lookupIDs), \
             "Added %s elements to modelCache; expected %s." % \
             (len(self.__modelCache), len(lookupIDs))

      if self.debug:
        _emit(Verbosity.DEBUG,
              "MODELITERATOR: Leaving __fillCache(); modelCacheLen=%s" % \
                (len(self.__modelCache),))


  return ModelInfoIterator(modelIDs)