def makeSearchJobParamsDict(cls, options, forRunning=False):
    """Constructs a dictionary of HyperSearch parameters suitable for converting
    to json and passing as the params argument to ClientJobsDAO.jobInsert()
    Parameters:
    ----------------------------------------------------------------------
    options:        NupicRunPermutations options dict
    forRunning:     True if the params are for running a Hypersearch job; False
                    if params are for introspection only.

    retval:         A dictionary of HyperSearch parameters for
                    ClientJobsDAO.jobInsert()
    """
    if options["searchMethod"] == "v2":
      hsVersion = "v2"
    else:
      raise Exception("Unsupported search method: %r" % options["searchMethod"])

    maxModels = options["maxPermutations"]
    if options["action"] == "dryRun" and maxModels is None:
      maxModels = 1

    useTerminators = options["useTerminators"]
    if useTerminators is None:
      params = {
              "hsVersion":          hsVersion,
              "maxModels":          maxModels,
             }
    else:
      params = {
              "hsVersion":          hsVersion,
              "useTerminators":     useTerminators,
              "maxModels":          maxModels,
             }

    if forRunning:
      params["persistentJobGUID"] = str(uuid.uuid1())

    if options["permutationsScriptPath"]:
      params["permutationsPyFilename"] = options["permutationsScriptPath"]
    elif options["expDescConfig"]:
      params["description"] = options["expDescConfig"]
    else:
      with open(options["expDescJsonPath"], mode="r") as fp:
        params["description"] = json.load(fp)

    return params