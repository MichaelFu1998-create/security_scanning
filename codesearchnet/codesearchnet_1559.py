def _runExperimentImpl(options, model=None):
  """Creates and runs the experiment

  Args:
    options: namedtuple ParseCommandLineOptionsResult
    model: For testing: may pass in an existing OPF Model instance
        to use instead of creating a new one.

  Returns: reference to OPFExperiment instance that was constructed (this
      is provided to aid with debugging) or None, if none was
      created.
  """
  json_helpers.validate(options.privateOptions,
                        schemaDict=g_parsedPrivateCommandLineOptionsSchema)

  # Load the experiment's description.py module
  experimentDir = options.experimentDir
  descriptionPyModule = helpers.loadExperimentDescriptionScriptFromDir(
      experimentDir)
  expIface = helpers.getExperimentDescriptionInterfaceFromModule(
      descriptionPyModule)

  # Handle "list checkpoints" request
  if options.privateOptions['listAvailableCheckpoints']:
    _printAvailableCheckpoints(experimentDir)
    return None

  # Load experiment tasks
  experimentTasks = expIface.getModelControl().get('tasks', [])

  # If the tasks list is empty, and this is a nupic environment description
  # file being run from the OPF, convert it to a simple OPF description file.
  if (len(experimentTasks) == 0 and
      expIface.getModelControl()['environment'] == OpfEnvironment.Nupic):
    expIface.convertNupicEnvToOPF()
    experimentTasks = expIface.getModelControl().get('tasks', [])

  # Ensures all the source locations are either absolute paths or relative to
  # the nupic.datafiles package_data location.
  expIface.normalizeStreamSources()

  # Extract option
  newSerialization = options.privateOptions['newSerialization']

  # Handle listTasks
  if options.privateOptions['listTasks']:
    print "Available tasks:"

    for label in [t['taskLabel'] for t in experimentTasks]:
      print "\t", label

    return None

  # Construct the experiment instance
  if options.privateOptions['runCheckpointName']:

    assert model is None

    checkpointName = options.privateOptions['runCheckpointName']

    model = ModelFactory.loadFromCheckpoint(
          savedModelDir=_getModelCheckpointDir(experimentDir, checkpointName),
          newSerialization=newSerialization)

  elif model is not None:
    print "Skipping creation of OPFExperiment instance: caller provided his own"
  else:
    modelDescription = expIface.getModelDescription()
    model = ModelFactory.create(modelDescription)

  # Handle "create model" request
  if options.privateOptions['createCheckpointName']:
    checkpointName = options.privateOptions['createCheckpointName']
    _saveModel(model=model,
               experimentDir=experimentDir,
               checkpointLabel=checkpointName,
               newSerialization=newSerialization)

    return model

  # Build the task list

  # Default task execution index list is in the natural list order of the tasks
  taskIndexList = range(len(experimentTasks))

  customTaskExecutionLabelsList = options.privateOptions['taskLabels']
  if customTaskExecutionLabelsList:
    taskLabelsList = [t['taskLabel'] for t in experimentTasks]
    taskLabelsSet = set(taskLabelsList)

    customTaskExecutionLabelsSet = set(customTaskExecutionLabelsList)

    assert customTaskExecutionLabelsSet.issubset(taskLabelsSet), \
           ("Some custom-provided task execution labels don't correspond "
            "to actual task labels: mismatched labels: %r; actual task "
            "labels: %r.") % (customTaskExecutionLabelsSet - taskLabelsSet,
                              customTaskExecutionLabelsList)

    taskIndexList = [taskLabelsList.index(label) for label in
                     customTaskExecutionLabelsList]

    print "#### Executing custom task list: %r" % [taskLabelsList[i] for
                                                   i in taskIndexList]

  # Run all experiment tasks
  for taskIndex in taskIndexList:

    task = experimentTasks[taskIndex]

    # Create a task runner and run it!
    taskRunner = _TaskRunner(model=model,
                             task=task,
                             cmdOptions=options)
    taskRunner.run()
    del taskRunner

    if options.privateOptions['checkpointModel']:
      _saveModel(model=model,
                 experimentDir=experimentDir,
                 checkpointLabel=task['taskLabel'],
                 newSerialization=newSerialization)

  return model