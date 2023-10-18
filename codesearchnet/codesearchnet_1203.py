def _addAnomalyClassifierRegion(self, network, params, spEnable, tmEnable):
    """
    Attaches an 'AnomalyClassifier' region to the network. Will remove current
    'AnomalyClassifier' region if it exists.

    Parameters
    -----------
    network - network to add the AnomalyClassifier region
    params - parameters to pass to the region
    spEnable - True if network has an SP region
    tmEnable - True if network has a TM region; Currently requires True
    """

    allParams = copy.deepcopy(params)
    knnParams = dict(k=1,
                     distanceMethod='rawOverlap',
                     distanceNorm=1,
                     doBinarization=1,
                     replaceDuplicates=0,
                     maxStoredPatterns=1000)
    allParams.update(knnParams)

    # Set defaults if not set
    if allParams['trainRecords'] is None:
      allParams['trainRecords'] = DEFAULT_ANOMALY_TRAINRECORDS

    if allParams['cacheSize'] is None:
      allParams['cacheSize'] = DEFAULT_ANOMALY_CACHESIZE

    # Remove current instance if already created (used for deserializing)
    if self._netInfo is not None and self._netInfo.net is not None \
              and self._getAnomalyClassifier() is not None:
      self._netInfo.net.removeRegion('AnomalyClassifier')

    network.addRegion("AnomalyClassifier",
                      "py.KNNAnomalyClassifierRegion",
                      json.dumps(allParams))

    # Attach link to SP
    if spEnable:
      network.link("SP", "AnomalyClassifier", "UniformLink", "",
          srcOutput="bottomUpOut", destInput="spBottomUpOut")
    else:
      network.link("sensor", "AnomalyClassifier", "UniformLink", "",
          srcOutput="dataOut", destInput="spBottomUpOut")

    # Attach link to TM
    if tmEnable:
      network.link("TM", "AnomalyClassifier", "UniformLink", "",
              srcOutput="topDownOut", destInput="tpTopDownOut")
      network.link("TM", "AnomalyClassifier", "UniformLink", "",
              srcOutput="lrnActiveStateT", destInput="tpLrnActiveStateT")
    else:
      raise RuntimeError("TemporalAnomaly models require a TM region.")