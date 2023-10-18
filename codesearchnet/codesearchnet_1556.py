def _parseCommandLineOptions(args):
  """Parse command line options

  Args:
    args: command line arguments (not including sys.argv[0])
  Returns:
    namedtuple ParseCommandLineOptionsResult
  """
  usageStr = (
    "%prog [options] descriptionPyDirectory\n"
    "This script runs a single OPF Model described by description.py "
    "located in the given directory."
    )

  parser = optparse.OptionParser(usage=usageStr)

  parser.add_option("-c",
                    help="Create a model and save it under the given "
                         "<CHECKPOINT> name, but don't run it",
                    dest="createCheckpointName",
                    action="store", type="string", default="",
                    metavar="<CHECKPOINT>")

  parser.add_option("--listCheckpoints",
                    help="List all available checkpoints",
                    dest="listAvailableCheckpoints",
                    action="store_true", default=False)

  parser.add_option("--listTasks",
                    help="List all task labels in description.py",
                    dest="listTasks",
                    action="store_true", default=False)

  parser.add_option("--load",
                    help="Load a model from the given <CHECKPOINT> and run it. "
                         "Run with --listCheckpoints flag for more details. ",
                    dest="runCheckpointName",
                    action="store", type="string", default="",
                    metavar="<CHECKPOINT>")

  parser.add_option("--newSerialization",
                    help="Use new capnproto serialization",
                    dest="newSerialization",
                    action="store_true", default=False)

  #parser.add_option("--reuseDatasets",
  #                  help="Keep existing generated/aggregated datasets",
  #                  dest="reuseDatasets", action="store_true",
  #                  default=False)

  parser.add_option("--tasks",
                    help="Run the tasks with the given TASK LABELS "
                         "in the order they are given.  Either end of "
                         "arg-list, or a standalone dot ('.') arg or "
                         "the next short or long option name (-a or "
                         "--blah) terminates the list. NOTE: FAILS "
                         "TO RECOGNIZE task label names with one or more "
                         "leading dashes. [default: run all of the tasks in "
                         "description.py]",
                    dest="taskLabels", default=[],
                    action="callback", callback=reapVarArgsCallback,
                    metavar="TASK_LABELS")

  parser.add_option("--testMode",
                    help="Reduce iteration count for testing",
                    dest="testMode", action="store_true",
                    default=False)

  parser.add_option("--noCheckpoint",
                    help="Don't checkpoint the model after running each task.",
                    dest="checkpointModel", action="store_false",
                    default=True)

  options, experiments = parser.parse_args(args)

  # Validate args
  mutuallyExclusiveOptionCount = sum([bool(options.createCheckpointName),
                                      options.listAvailableCheckpoints,
                                      options.listTasks,
                                      bool(options.runCheckpointName)])
  if mutuallyExclusiveOptionCount > 1:
    _reportCommandLineUsageErrorAndExit(
        parser,
        "Options: -c, --listCheckpoints, --listTasks, and --load are "
        "mutually exclusive. Please select only one")

  mutuallyExclusiveOptionCount = sum([bool(not options.checkpointModel),
                                      bool(options.createCheckpointName)])
  if mutuallyExclusiveOptionCount > 1:
    _reportCommandLineUsageErrorAndExit(
        parser,
        "Options: -c and --noCheckpoint are "
        "mutually exclusive. Please select only one")

  if len(experiments) != 1:
    _reportCommandLineUsageErrorAndExit(
        parser,
        "Exactly ONE experiment must be specified, but got %s (%s)" % (
            len(experiments), experiments))

  # Done with parser
  parser.destroy()

  # Prepare results

  # Directory path of the experiment (that contain description.py)
  experimentDir = os.path.abspath(experiments[0])

  # RunExperiment.py's private options (g_parsedPrivateCommandLineOptionsSchema)
  privateOptions = dict()
  privateOptions['createCheckpointName'] = options.createCheckpointName
  privateOptions['listAvailableCheckpoints'] = options.listAvailableCheckpoints
  privateOptions['listTasks'] = options.listTasks
  privateOptions['runCheckpointName'] = options.runCheckpointName
  privateOptions['newSerialization'] = options.newSerialization
  privateOptions['testMode'] = options.testMode
  #privateOptions['reuseDatasets']  = options.reuseDatasets
  privateOptions['taskLabels'] = options.taskLabels
  privateOptions['checkpointModel'] = options.checkpointModel

  result = ParseCommandLineOptionsResult(experimentDir=experimentDir,
                                         privateOptions=privateOptions)
  return result