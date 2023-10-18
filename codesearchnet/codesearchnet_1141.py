def queryModelIDs(self):
    """Queuries DB for model IDs of all currently instantiated models
    associated with this HyperSearch job.

    See also: _iterModels()

    Parameters:
    ----------------------------------------------------------------------
    retval:         A sequence of Nupic modelIDs
    """
    jobID = self.getJobID()
    modelCounterPairs = _clientJobsDB().modelsGetUpdateCounters(jobID)
    modelIDs = tuple(x[0] for x in modelCounterPairs)

    return modelIDs