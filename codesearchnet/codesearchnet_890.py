def runModelGivenBaseAndParams(modelID, jobID, baseDescription, params,
            predictedField, reportKeys, optimizeKey, jobsDAO,
            modelCheckpointGUID, logLevel=None, predictionCacheMaxRecords=None):
  """ This creates an experiment directory with a base.py description file
  created from 'baseDescription' and a description.py generated from the
  given params dict and then runs the experiment.

  Parameters:
  -------------------------------------------------------------------------
  modelID:              ID for this model in the models table
  jobID:                ID for this hypersearch job in the jobs table
  baseDescription:      Contents of a description.py with the base experiment
                                          description
  params:               Dictionary of specific parameters to override within
                                  the baseDescriptionFile.
  predictedField:       Name of the input field for which this model is being
                                    optimized
  reportKeys:           Which metrics of the experiment to store into the
                                    results dict of the model's database entry
  optimizeKey:          Which metric we are optimizing for
  jobsDAO               Jobs data access object - the interface to the
                                  jobs database which has the model's table.
  modelCheckpointGUID:  A persistent, globally-unique identifier for
                                  constructing the model checkpoint key
  logLevel:             override logging level to this value, if not None

  retval:               (completionReason, completionMsg)
  """
  from nupic.swarming.ModelRunner import OPFModelRunner

  # The logger for this method
  logger = logging.getLogger('com.numenta.nupic.hypersearch.utils')


  # --------------------------------------------------------------------------
  # Create a temp directory for the experiment and the description files
  experimentDir = tempfile.mkdtemp()
  try:
    logger.info("Using experiment directory: %s" % (experimentDir))

    # Create the decription.py from the overrides in params
    paramsFilePath = os.path.join(experimentDir, 'description.py')
    paramsFile = open(paramsFilePath, 'wb')
    paramsFile.write(_paramsFileHead())

    items = params.items()
    items.sort()
    for (key,value) in items:
      quotedKey = _quoteAndEscape(key)
      if isinstance(value, basestring):

        paramsFile.write("  %s : '%s',\n" % (quotedKey , value))
      else:
        paramsFile.write("  %s : %s,\n" % (quotedKey , value))

    paramsFile.write(_paramsFileTail())
    paramsFile.close()


    # Write out the base description
    baseParamsFile = open(os.path.join(experimentDir, 'base.py'), 'wb')
    baseParamsFile.write(baseDescription)
    baseParamsFile.close()


    # Store the experiment's sub-description file into the model table
    #  for reference
    fd = open(paramsFilePath)
    expDescription = fd.read()
    fd.close()
    jobsDAO.modelSetFields(modelID, {'genDescription': expDescription})


    # Run the experiment now
    try:
      runner = OPFModelRunner(
        modelID=modelID,
        jobID=jobID,
        predictedField=predictedField,
        experimentDir=experimentDir,
        reportKeyPatterns=reportKeys,
        optimizeKeyPattern=optimizeKey,
        jobsDAO=jobsDAO,
        modelCheckpointGUID=modelCheckpointGUID,
        logLevel=logLevel,
        predictionCacheMaxRecords=predictionCacheMaxRecords)

      signal.signal(signal.SIGINT, runner.handleWarningSignal)

      (completionReason, completionMsg) = runner.run()

    except InvalidConnectionException:
      raise
    except Exception, e:

      (completionReason, completionMsg) = _handleModelRunnerException(jobID,
                                     modelID, jobsDAO, experimentDir, logger, e)

  finally:
    # delete our temporary directory tree
    shutil.rmtree(experimentDir)
    signal.signal(signal.SIGINT, signal.default_int_handler)

  # Return completion reason and msg
  return (completionReason, completionMsg)