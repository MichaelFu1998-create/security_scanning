def runWithConfig(swarmConfig, options,
                  outDir=None, outputLabel="default",
                  permWorkDir=None, verbosity=1):
  """
  Starts a swarm, given an dictionary configuration.
  @param swarmConfig {dict} A complete [swarm description](http://nupic.docs.numenta.org/0.7.0.dev0/guides/swarming/running.html#the-swarm-description) object.
  @param outDir {string} Optional path to write swarm details (defaults to
                         current working directory).
  @param outputLabel {string} Optional label for output (defaults to "default").
  @param permWorkDir {string} Optional location of working directory (defaults
                              to current working directory).
  @param verbosity {int} Optional (1,2,3) increasing verbosity of output.

  @returns {object} Model parameters
  """
  global g_currentVerbosityLevel
  g_currentVerbosityLevel = verbosity

  # Generate the description and permutations.py files in the same directory
  #  for reference.
  if outDir is None:
    outDir = os.getcwd()
  if permWorkDir is None:
    permWorkDir = os.getcwd()

  _checkOverwrite(options, outDir)

  _generateExpFilesFromSwarmDescription(swarmConfig, outDir)

  options["expDescConfig"] = swarmConfig
  options["outputLabel"] = outputLabel
  options["outDir"] = outDir
  options["permWorkDir"] = permWorkDir

  runOptions = _injectDefaultOptions(options)
  _validateOptions(runOptions)

  return _runAction(runOptions)