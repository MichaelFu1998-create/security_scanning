def runWithPermutationsScript(permutationsFilePath, options,
                                 outputLabel, permWorkDir):
  """
  Starts a swarm, given a path to a permutations.py script.

  This function is meant to be used with a CLI wrapper that passes command line
  arguments in through the options parameter.

  @param permutationsFilePath {string} Path to permutations.py.
  @param options {dict} CLI options.
  @param outputLabel {string} Label for output.
  @param permWorkDir {string} Location of working directory.

  @returns {object} Model parameters.
  """
  global g_currentVerbosityLevel
  if "verbosityCount" in options:
    g_currentVerbosityLevel = options["verbosityCount"]
    del options["verbosityCount"]
  else:
    g_currentVerbosityLevel = 1

  _setupInterruptHandling()

  options["permutationsScriptPath"] = permutationsFilePath
  options["outputLabel"] = outputLabel
  options["outDir"] = permWorkDir
  options["permWorkDir"] = permWorkDir

  # Assume it's a permutations python script
  runOptions = _injectDefaultOptions(options)
  _validateOptions(runOptions)

  return _runAction(runOptions)