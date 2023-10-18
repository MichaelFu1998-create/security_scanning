def _getClassifierRegion(self):
    """
    Returns reference to the network's Classifier region
    """
    if (self._netInfo.net is not None and
        "Classifier" in self._netInfo.net.regions):
      return self._netInfo.net.regions["Classifier"]
    else:
      return None