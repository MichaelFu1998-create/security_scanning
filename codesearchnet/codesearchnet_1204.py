def __getNetworkStateDirectory(self, extraDataDir):
    """
    extraDataDir:
                  Model's extra data directory path
    Returns:      Absolute directory path for saving CLA Network
    """
    if self.__restoringFromV1:
      if self.getInferenceType() == InferenceType.TemporalNextStep:
        leafName = 'temporal'+ "-network.nta"
      else:
        leafName = 'nonTemporal'+ "-network.nta"
    else:
      leafName = InferenceType.getLabel(self.getInferenceType()) + "-network.nta"
    path = os.path.join(extraDataDir, leafName)
    path = os.path.abspath(path)
    return path