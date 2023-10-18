def loadExperiment(path):
  """Loads the experiment description file from the path.

  :param path: (string) The path to a directory containing a description.py file
         or the file itself.
  :returns: (config, control)
  """
  if not os.path.isdir(path):
    path = os.path.dirname(path)
  descriptionPyModule = loadExperimentDescriptionScriptFromDir(path)
  expIface = getExperimentDescriptionInterfaceFromModule(descriptionPyModule)
  return expIface.getModelDescription(), expIface.getModelControl()