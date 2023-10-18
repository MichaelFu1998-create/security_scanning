def createTemporalAnomaly(recordParams, spatialParams=_SP_PARAMS,
                          temporalParams=_TM_PARAMS,
                          verbosity=_VERBOSITY):


  """Generates a Network with connected RecordSensor, SP, TM.

  This function takes care of generating regions and the canonical links.
  The network has a sensor region reading data from a specified input and
  passing the encoded representation to an SPRegion.
  The SPRegion output is passed to a TMRegion.

  Note: this function returns a network that needs to be initialized. This
  allows the user to extend the network by adding further regions and
  connections.

  :param recordParams: a dict with parameters for creating RecordSensor region.
  :param spatialParams: a dict with parameters for creating SPRegion.
  :param temporalParams: a dict with parameters for creating TMRegion.
  :param verbosity: an integer representing how chatty the network will be.
  """
  inputFilePath = recordParams["inputFilePath"]
  scalarEncoderArgs = recordParams["scalarEncoderArgs"]
  dateEncoderArgs = recordParams["dateEncoderArgs"]

  scalarEncoder = ScalarEncoder(**scalarEncoderArgs)
  dateEncoder = DateEncoder(**dateEncoderArgs)

  encoder = MultiEncoder()
  encoder.addEncoder(scalarEncoderArgs["name"], scalarEncoder)
  encoder.addEncoder(dateEncoderArgs["name"], dateEncoder)

  network = Network()

  network.addRegion("sensor", "py.RecordSensor",
                    json.dumps({"verbosity": verbosity}))

  sensor = network.regions["sensor"].getSelf()
  sensor.encoder = encoder
  sensor.dataSource = FileRecordStream(streamID=inputFilePath)

  # Create the spatial pooler region
  spatialParams["inputWidth"] = sensor.encoder.getWidth()
  network.addRegion("spatialPoolerRegion", "py.SPRegion",
                    json.dumps(spatialParams))

  # Link the SP region to the sensor input
  network.link("sensor", "spatialPoolerRegion", "UniformLink", "")
  network.link("sensor", "spatialPoolerRegion", "UniformLink", "",
               srcOutput="resetOut", destInput="resetIn")
  network.link("spatialPoolerRegion", "sensor", "UniformLink", "",
               srcOutput="spatialTopDownOut", destInput="spatialTopDownIn")
  network.link("spatialPoolerRegion", "sensor", "UniformLink", "",
               srcOutput="temporalTopDownOut", destInput="temporalTopDownIn")

  # Add the TPRegion on top of the SPRegion
  network.addRegion("temporalPoolerRegion", "py.TMRegion",
                    json.dumps(temporalParams))

  network.link("spatialPoolerRegion", "temporalPoolerRegion", "UniformLink", "")
  network.link("temporalPoolerRegion", "spatialPoolerRegion", "UniformLink", "",
               srcOutput="topDownOut", destInput="topDownIn")

  spatialPoolerRegion = network.regions["spatialPoolerRegion"]

  # Make sure learning is enabled
  spatialPoolerRegion.setParameter("learningMode", True)
  # We want temporal anomalies so disable anomalyMode in the SP. This mode is
  # used for computing anomalies in a non-temporal model.
  spatialPoolerRegion.setParameter("anomalyMode", False)

  temporalPoolerRegion = network.regions["temporalPoolerRegion"]

  # Enable topDownMode to get the predicted columns output
  temporalPoolerRegion.setParameter("topDownMode", True)
  # Make sure learning is enabled (this is the default)
  temporalPoolerRegion.setParameter("learningMode", True)
  # Enable inference mode so we get predictions
  temporalPoolerRegion.setParameter("inferenceMode", True)
  # Enable anomalyMode to compute the anomaly score.
  temporalPoolerRegion.setParameter("anomalyMode", True)

  return network