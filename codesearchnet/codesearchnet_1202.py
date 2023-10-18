def _deSerializeExtraData(self, extraDataDir):
    """ [virtual method override] This method is called during deserialization
    (after __setstate__) with an external directory path that can be used to
    bypass pickle for loading large binary states.

    extraDataDir:
                  Model's extra data directory path
    """
    assert self.__restoringFromState

    #--------------------------------------------------
    # Check to make sure that our Network member wasn't restored from
    # serialized data
    assert (self._netInfo.net is None), "Network was already unpickled"

    #--------------------------------------------------
    # Restore the network
    stateDir = self.__getNetworkStateDirectory(extraDataDir=extraDataDir)

    self.__logger.debug(
      "(%s) De-serializing network...", self)

    self._netInfo.net = Network(stateDir)

    self.__logger.debug(
      "(%s) Finished de-serializing network", self)


    # NuPIC doesn't initialize the network until you try to run it
    # but users may want to access components in a setup callback
    self._netInfo.net.initialize()


    # Used for backwards compatibility for anomaly classification models.
    # Previous versions used the HTMPredictionModelClassifierHelper class for utilizing
    # the KNN classifier. Current version uses KNNAnomalyClassifierRegion to
    # encapsulate all the classifier functionality.
    if self.getInferenceType() == InferenceType.TemporalAnomaly:
      classifierType = self._getAnomalyClassifier().getSelf().__class__.__name__
      if classifierType is 'KNNClassifierRegion':

        anomalyClParams = dict(
          trainRecords=self._classifier_helper._autoDetectWaitRecords,
          cacheSize=self._classifier_helper._history_length,
        )

        spEnable = (self._getSPRegion() is not None)
        tmEnable = True

        # Store original KNN region
        knnRegion = self._getAnomalyClassifier().getSelf()

        # Add new KNNAnomalyClassifierRegion
        self._addAnomalyClassifierRegion(self._netInfo.net, anomalyClParams,
                                         spEnable, tmEnable)

        # Restore state
        self._getAnomalyClassifier().getSelf()._iteration = self.__numRunCalls
        self._getAnomalyClassifier().getSelf()._recordsCache = (
            self._classifier_helper.saved_states)
        self._getAnomalyClassifier().getSelf().saved_categories = (
            self._classifier_helper.saved_categories)
        self._getAnomalyClassifier().getSelf()._knnclassifier = knnRegion

        # Set TM to output neccessary information
        self._getTPRegion().setParameter('anomalyMode', True)

        # Remove old classifier_helper
        del self._classifier_helper

        self._netInfo.net.initialize()

    #--------------------------------------------------
    # Mark end of restoration from state
    self.__restoringFromState = False

    self.__logger.debug("(%s) Finished restoring from state", self)

    return