def __loadHyperSearchJobID(cls, permWorkDir, outputLabel):
    """Loads a saved jobID from file

    Parameters:
    ----------------------------------------------------------------------
    permWorkDir:  Directory path for saved jobID file
    outputLabel:  Label string for incorporating into file name for saved jobID
    retval:       HyperSearch jobID; raises exception if not found.
    """
    filePath = cls.__getHyperSearchJobIDFilePath(permWorkDir=permWorkDir,
                                                 outputLabel=outputLabel)

    jobID = None
    with open(filePath, "r") as jobIdPickleFile:
      jobInfo = pickle.load(jobIdPickleFile)
      jobID = jobInfo["hyperSearchJobID"]

    return jobID