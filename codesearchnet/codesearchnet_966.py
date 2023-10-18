def _handleDescriptionOption(cmdArgStr, outDir, usageStr, hsVersion,
                             claDescriptionTemplateFile):
  """
  Parses and validates the --description option args and executes the
  request

  Parameters:
  -----------------------------------------------------------------------
  cmdArgStr:  JSON string compatible with _gExperimentDescriptionSchema
  outDir:     where to place generated experiment files
  usageStr:   program usage string
  hsVersion:  which version of hypersearch permutations file to generate, can
                be 'v1' or 'v2'
  claDescriptionTemplateFile: Filename containing the template description
  retval:     nothing


  """
  # convert --description arg from JSON string to dict
  try:
    args = json.loads(cmdArgStr)
  except Exception, e:
    raise _InvalidCommandArgException(
      _makeUsageErrorStr(
        ("JSON arg parsing failed for --description: %s\n" + \
         "ARG=<%s>") % (str(e), cmdArgStr), usageStr))

  #print "PARSED JSON ARGS=\n%s" % (json.dumps(args, indent=4))

  filesDescription = _generateExperiment(args, outDir, hsVersion=hsVersion,
                    claDescriptionTemplateFile = claDescriptionTemplateFile)

  pprint.pprint(filesDescription)

  return