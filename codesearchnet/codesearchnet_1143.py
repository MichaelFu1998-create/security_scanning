def getOptimizationMetricInfo(cls, searchJobParams):
    """Retrives the optimization key name and optimization function.

    Parameters:
    ---------------------------------------------------------
    searchJobParams:
                    Parameter for passing as the searchParams arg to
                    Hypersearch constructor.
    retval:       (optimizationMetricKey, maximize)
                  optimizationMetricKey: which report key to optimize for
                  maximize: True if we should try and maximize the optimizeKey
                    metric. False if we should minimize it.
    """
    if searchJobParams["hsVersion"] == "v2":
      search = HypersearchV2(searchParams=searchJobParams)
    else:
      raise RuntimeError("Unsupported hypersearch version \"%s\"" % \
                         (searchJobParams["hsVersion"]))

    info = search.getOptimizationMetricInfo()
    return info