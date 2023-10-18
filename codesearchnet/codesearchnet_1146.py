def __unwrapParams(self):
    """Unwraps self.__rawInfo.params into the equivalent python dictionary
    and caches it in self.__cachedParams. Returns the unwrapped params

    Parameters:
    ----------------------------------------------------------------------
    retval:         Model params dictionary as correpsonding to the json
                    as returned in ClientJobsDAO.modelsInfo()[x].params
    """
    if self.__cachedParams is None:
      self.__cachedParams = json.loads(self.__rawInfo.params)
      assert self.__cachedParams is not None, \
             "%s resulted in None" % self.__rawInfo.params

    return self.__cachedParams