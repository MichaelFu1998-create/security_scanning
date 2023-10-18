def __unwrapResults(self):
    """Unwraps self.__rawInfo.results and caches it in self.__cachedResults;
    Returns the unwrapped params

    Parameters:
    ----------------------------------------------------------------------
    retval:         ModelResults namedtuple instance
    """
    if self.__cachedResults is None:
      if self.__rawInfo.results is not None:
        resultList = json.loads(self.__rawInfo.results)
        assert len(resultList) == 2, \
               "Expected 2 elements, but got %s (%s)." % (
                len(resultList), resultList)
        self.__cachedResults = self.ModelResults(
          reportMetrics=resultList[0],
          optimizationMetrics=resultList[1])
      else:
        self.__cachedResults = self.ModelResults(
          reportMetrics={},
          optimizationMetrics={})


    return self.__cachedResults