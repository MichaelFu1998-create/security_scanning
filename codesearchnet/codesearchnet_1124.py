def runWithJsonFile(expJsonFilePath, options, outputLabel, permWorkDir):
  """
  Starts a swarm, given a path to a JSON file containing configuration.

  This function is meant to be used with a CLI wrapper that passes command line
  arguments in through the options parameter.

  @param expJsonFilePath {string} Path to a JSON file containing the complete
                                 [swarm description](http://nupic.docs.numenta.org/0.7.0.dev0/guides/swarming/running.html#the-swarm-description).
  @param options {dict} CLI options.
  @param outputLabel {string} Label for output.
  @param permWorkDir {string} Location of working directory.

  @returns {int} Swarm job id.
  """
  if "verbosityCount" in options:
    verbosity = options["verbosityCount"]
    del options["verbosityCount"]
  else:
    verbosity = 1

  _setupInterruptHandling()

  with open(expJsonFilePath, "r") as jsonFile:
    expJsonConfig = json.loads(jsonFile.read())

  outDir = os.path.dirname(expJsonFilePath)
  return runWithConfig(expJsonConfig, options, outDir=outDir,
                       outputLabel=outputLabel, permWorkDir=permWorkDir,
                       verbosity=verbosity)