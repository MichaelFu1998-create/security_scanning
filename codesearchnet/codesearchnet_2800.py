def get_tmaster(self, topologyName, callback=None):
    """
    Get tmaster
    """
    if callback:
      self.tmaster_watchers[topologyName].append(callback)
    else:
      tmaster_path = self.get_tmaster_path(topologyName)
      with open(tmaster_path) as f:
        data = f.read()
        tmaster = TMasterLocation()
        tmaster.ParseFromString(data)
        return tmaster