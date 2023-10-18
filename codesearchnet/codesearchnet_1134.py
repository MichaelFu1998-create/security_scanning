def __saveHyperSearchJobID(cls, permWorkDir, outputLabel, hyperSearchJob):
    """Saves the given _HyperSearchJob instance's jobID to file

    Parameters:
    ----------------------------------------------------------------------
    permWorkDir:   Directory path for saved jobID file
    outputLabel:   Label string for incorporating into file name for saved jobID
    hyperSearchJob: _HyperSearchJob instance
    retval:        nothing
    """
    jobID = hyperSearchJob.getJobID()
    filePath = cls.__getHyperSearchJobIDFilePath(permWorkDir=permWorkDir,
                                                 outputLabel=outputLabel)

    if os.path.exists(filePath):
      _backupFile(filePath)

    d = dict(hyperSearchJobID = jobID)

    with open(filePath, "wb") as jobIdPickleFile:
      pickle.dump(d, jobIdPickleFile)