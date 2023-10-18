def loadExperimentDescriptionScriptFromDir(experimentDir):
  """ Loads the experiment description python script from the given experiment
  directory.

  :param experimentDir: (string) experiment directory path

  :returns:        module of the loaded experiment description scripts
  """
  descriptionScriptPath = os.path.join(experimentDir, "description.py")
  module = _loadDescriptionFile(descriptionScriptPath)
  return module