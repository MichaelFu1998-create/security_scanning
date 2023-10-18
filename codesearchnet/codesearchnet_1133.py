def loadSavedHyperSearchJob(cls, permWorkDir, outputLabel):
    """Instantiates a _HyperSearchJob instance from info saved in file

    Parameters:
    ----------------------------------------------------------------------
    permWorkDir: Directory path for saved jobID file
    outputLabel: Label string for incorporating into file name for saved jobID
    retval:      _HyperSearchJob instance; raises exception if not found
    """
    jobID = cls.__loadHyperSearchJobID(permWorkDir=permWorkDir,
                                       outputLabel=outputLabel)

    searchJob = _HyperSearchJob(nupicJobID=jobID)
    return searchJob