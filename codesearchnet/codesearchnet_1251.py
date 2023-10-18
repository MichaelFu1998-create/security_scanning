def createNetwork(dataSource):
  """Creates and returns a new Network with a sensor region reading data from
  'dataSource'. There are two hierarchical levels, each with one SP and one TM.
  @param dataSource - A RecordStream containing the input data
  @returns a Network ready to run
  """
  network = Network()

  # Create and add a record sensor and a SP region
  sensor = createRecordSensor(network, name=_RECORD_SENSOR,
                              dataSource=dataSource)
  createSpatialPooler(network, name=_L1_SPATIAL_POOLER,
                      inputWidth=sensor.encoder.getWidth())

  # Link the SP region to the sensor input
  linkType = "UniformLink"
  linkParams = ""
  network.link(_RECORD_SENSOR, _L1_SPATIAL_POOLER, linkType, linkParams)

  # Create and add a TM region
  l1temporalMemory = createTemporalMemory(network, _L1_TEMPORAL_MEMORY)

  # Link SP region to TM region in the feedforward direction
  network.link(_L1_SPATIAL_POOLER, _L1_TEMPORAL_MEMORY, linkType, linkParams)

  # Add a classifier
  classifierParams = {  # Learning rate. Higher values make it adapt faster.
                        'alpha': 0.005,

                        # A comma separated list of the number of steps the
                        # classifier predicts in the future. The classifier will
                        # learn predictions of each order specified.
                        'steps': '1',

                        # The specific implementation of the classifier to use
                        # See SDRClassifierFactory#create for options
                        'implementation': 'py',

                        # Diagnostic output verbosity control;
                        # 0: silent; [1..6]: increasing levels of verbosity
                        'verbosity': 0}

  l1Classifier = network.addRegion(_L1_CLASSIFIER, "py.SDRClassifierRegion",
                                   json.dumps(classifierParams))
  l1Classifier.setParameter('inferenceMode', True)
  l1Classifier.setParameter('learningMode', True)
  network.link(_L1_TEMPORAL_MEMORY, _L1_CLASSIFIER, linkType, linkParams,
               srcOutput="bottomUpOut", destInput="bottomUpIn")
  network.link(_RECORD_SENSOR, _L1_CLASSIFIER, linkType, linkParams,
               srcOutput="categoryOut", destInput="categoryIn")
  network.link(_RECORD_SENSOR, _L1_CLASSIFIER, linkType, linkParams,
               srcOutput="bucketIdxOut", destInput="bucketIdxIn")
  network.link(_RECORD_SENSOR, _L1_CLASSIFIER, linkType, linkParams,
               srcOutput="actValueOut", destInput="actValueIn")

  # Second Level
  l2inputWidth = l1temporalMemory.getSelf().getOutputElementCount("bottomUpOut")
  createSpatialPooler(network, name=_L2_SPATIAL_POOLER, inputWidth=l2inputWidth)
  network.link(_L1_TEMPORAL_MEMORY, _L2_SPATIAL_POOLER, linkType, linkParams)

  createTemporalMemory(network, _L2_TEMPORAL_MEMORY)
  network.link(_L2_SPATIAL_POOLER, _L2_TEMPORAL_MEMORY, linkType, linkParams)

  l2Classifier = network.addRegion(_L2_CLASSIFIER, "py.SDRClassifierRegion",
                                   json.dumps(classifierParams))
  l2Classifier.setParameter('inferenceMode', True)
  l2Classifier.setParameter('learningMode', True)
  network.link(_L2_TEMPORAL_MEMORY, _L2_CLASSIFIER, linkType, linkParams,
               srcOutput="bottomUpOut", destInput="bottomUpIn")
  network.link(_RECORD_SENSOR, _L2_CLASSIFIER, linkType, linkParams,
               srcOutput="categoryOut", destInput="categoryIn")
  network.link(_RECORD_SENSOR, _L2_CLASSIFIER, linkType, linkParams,
               srcOutput="bucketIdxOut", destInput="bucketIdxIn")
  network.link(_RECORD_SENSOR, _L2_CLASSIFIER, linkType, linkParams,
               srcOutput="actValueOut", destInput="actValueIn")
  return network