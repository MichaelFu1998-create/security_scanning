def _handleDescriptionFromFileOption(filename, outDir, usageStr, hsVersion,
                             claDescriptionTemplateFile):
  """
  Parses and validates the --descriptionFromFile option and executes the
  request

  Parameters:
  -----------------------------------------------------------------------
  filename:   File from which we'll extract description JSON
  outDir:     where to place generated experiment files
  usageStr:   program usage string
  hsVersion:  which version of hypersearch permutations file to generate, can
                be 'v1' or 'v2'
  claDescriptionTemplateFile: Filename containing the template description
  retval:     nothing
  """

  try:
    fileHandle = open(filename, 'r')
    JSONStringFromFile = fileHandle.read().splitlines()
    JSONStringFromFile = ''.join(JSONStringFromFile)

  except Exception, e:
    raise _InvalidCommandArgException(
      _makeUsageErrorStr(
        ("File open failed for --descriptionFromFile: %s\n" + \
         "ARG=<%s>") % (str(e), filename), usageStr))

  _handleDescriptionOption(JSONStringFromFile, outDir, usageStr,
        hsVersion=hsVersion,
        claDescriptionTemplateFile = claDescriptionTemplateFile)
  return