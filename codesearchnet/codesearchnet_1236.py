def createExperimentInferenceDir(cls, experimentDir):
    """ Creates the inference output directory for the given experiment

    experimentDir:  experiment directory path that contains description.py

    Returns:  path of the inference output directory
    """
    path = cls.getExperimentInferenceDirPath(experimentDir)

    cls.makeDirectory(path)

    return path