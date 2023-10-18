def _loadDescriptionFile(descriptionPyPath):
  """Loads a description file and returns it as a module.

  descriptionPyPath: path of description.py file to load
  """
  global g_descriptionImportCount

  if not os.path.isfile(descriptionPyPath):
    raise RuntimeError(("Experiment description file %s does not exist or " + \
                        "is not a file") % (descriptionPyPath,))

  mod = imp.load_source("pf_description%d" % g_descriptionImportCount,
                        descriptionPyPath)
  g_descriptionImportCount += 1

  if not hasattr(mod, "descriptionInterface"):
    raise RuntimeError("Experiment description file %s does not define %s" % \
                       (descriptionPyPath, "descriptionInterface"))

  if not isinstance(mod.descriptionInterface, exp_description_api.DescriptionIface):
    raise RuntimeError(("Experiment description file %s defines %s but it " + \
                        "is not DescriptionIface-based") % \
                            (descriptionPyPath, name))

  return mod