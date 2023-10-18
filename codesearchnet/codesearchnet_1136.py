def __getHyperSearchJobIDFilePath(cls, permWorkDir, outputLabel):
    """Returns filepath where to store HyperSearch JobID

    Parameters:
    ----------------------------------------------------------------------
    permWorkDir: Directory path for saved jobID file
    outputLabel: Label string for incorporating into file name for saved jobID
    retval:      Filepath where to store HyperSearch JobID
    """
    # Get the base path and figure out the path of the report file.
    basePath = permWorkDir

    # Form the name of the output csv file that will contain all the results
    filename = "%s_HyperSearchJobID.pkl" % (outputLabel,)
    filepath = os.path.join(basePath, filename)

    return filepath