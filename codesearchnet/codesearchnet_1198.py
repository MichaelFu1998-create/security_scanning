def __createHTMNetwork(self, sensorParams, spEnable, spParams, tmEnable,
                         tmParams, clEnable, clParams, anomalyParams):
    """ Create a CLA network and return it.

    description:  HTMPredictionModel description dictionary (TODO: define schema)
    Returns:      NetworkInfo instance;
    """

    #--------------------------------------------------
    # Create the network
    n = Network()


    #--------------------------------------------------
    # Add the Sensor
    n.addRegion("sensor", "py.RecordSensor", json.dumps(dict(verbosity=sensorParams['verbosity'])))
    sensor = n.regions['sensor'].getSelf()

    enabledEncoders = copy.deepcopy(sensorParams['encoders'])
    for name, params in enabledEncoders.items():
      if params is not None:
        classifierOnly = params.pop('classifierOnly', False)
        if classifierOnly:
          enabledEncoders.pop(name)

    # Disabled encoders are encoders that are fed to SDRClassifierRegion but not
    # SP or TM Regions. This is to handle the case where the predicted field
    # is not fed through the SP/TM. We typically just have one of these now.
    disabledEncoders = copy.deepcopy(sensorParams['encoders'])
    for name, params in disabledEncoders.items():
      if params is None:
        disabledEncoders.pop(name)
      else:
        classifierOnly = params.pop('classifierOnly', False)
        if not classifierOnly:
          disabledEncoders.pop(name)

    encoder = MultiEncoder(enabledEncoders)

    sensor.encoder = encoder
    sensor.disabledEncoder = MultiEncoder(disabledEncoders)
    sensor.dataSource = DataBuffer()

    prevRegion = "sensor"
    prevRegionWidth = encoder.getWidth()

    # SP is not enabled for spatial classification network
    if spEnable:
      spParams = spParams.copy()
      spParams['inputWidth'] = prevRegionWidth
      self.__logger.debug("Adding SPRegion; spParams: %r" % spParams)
      n.addRegion("SP", "py.SPRegion", json.dumps(spParams))

      # Link SP region
      n.link("sensor", "SP", "UniformLink", "")
      n.link("sensor", "SP", "UniformLink", "", srcOutput="resetOut",
             destInput="resetIn")

      n.link("SP", "sensor", "UniformLink", "", srcOutput="spatialTopDownOut",
             destInput="spatialTopDownIn")
      n.link("SP", "sensor", "UniformLink", "", srcOutput="temporalTopDownOut",
             destInput="temporalTopDownIn")

      prevRegion = "SP"
      prevRegionWidth = spParams['columnCount']

    if tmEnable:
      tmParams = tmParams.copy()
      if prevRegion == 'sensor':
        tmParams['inputWidth'] = tmParams['columnCount'] = prevRegionWidth
      else:
        assert tmParams['columnCount'] == prevRegionWidth
        tmParams['inputWidth'] = tmParams['columnCount']

      self.__logger.debug("Adding TMRegion; tmParams: %r" % tmParams)
      n.addRegion("TM", "py.TMRegion", json.dumps(tmParams))

      # Link TM region
      n.link(prevRegion, "TM", "UniformLink", "")
      if prevRegion != "sensor":
        n.link("TM", prevRegion, "UniformLink", "", srcOutput="topDownOut",
           destInput="topDownIn")
      else:
        n.link("TM", prevRegion, "UniformLink", "", srcOutput="topDownOut",
           destInput="temporalTopDownIn")
      n.link("sensor", "TM", "UniformLink", "", srcOutput="resetOut",
         destInput="resetIn")

      prevRegion = "TM"
      prevRegionWidth = tmParams['inputWidth']

    if clEnable and clParams is not None:
      clParams = clParams.copy()
      clRegionName = clParams.pop('regionName')
      self.__logger.debug("Adding %s; clParams: %r" % (clRegionName,
                                                      clParams))
      n.addRegion("Classifier", "py.%s" % str(clRegionName), json.dumps(clParams))

      # SDR Classifier-specific links
      if str(clRegionName) == "SDRClassifierRegion":
        n.link("sensor", "Classifier", "UniformLink", "", srcOutput="actValueOut",
               destInput="actValueIn")
        n.link("sensor", "Classifier", "UniformLink", "", srcOutput="bucketIdxOut",
               destInput="bucketIdxIn")

      # This applies to all (SDR and KNN) classifiers
      n.link("sensor", "Classifier", "UniformLink", "", srcOutput="categoryOut",
             destInput="categoryIn")

      n.link(prevRegion, "Classifier", "UniformLink", "")

    if self.getInferenceType() == InferenceType.TemporalAnomaly:
      anomalyClParams = dict(
          trainRecords=anomalyParams.get('autoDetectWaitRecords', None),
          cacheSize=anomalyParams.get('anomalyCacheRecords', None)
      )
      self._addAnomalyClassifierRegion(n, anomalyClParams, spEnable, tmEnable)

    #--------------------------------------------------
    # NuPIC doesn't initialize the network until you try to run it
    # but users may want to access components in a setup callback
    n.initialize()

    return NetworkInfo(net=n, statsCollectors=[])