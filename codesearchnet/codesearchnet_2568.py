def _get_tmaster_with_watch(self, topologyName, callback, isWatching):
    """
    Helper function to get pplan with
    a callback. The future watch is placed
    only if isWatching is True.
    """
    path = self.get_tmaster_path(topologyName)
    if isWatching:
      LOG.info("Adding data watch for path: " + path)

    # pylint: disable=unused-variable, unused-argument
    @self.client.DataWatch(path)
    def watch_tmaster(data, stats):
      """ invoke callback to watch tmaster """
      if data:
        tmaster = TMasterLocation()
        tmaster.ParseFromString(data)
        callback(tmaster)
      else:
        callback(None)

      # Returning False will result in no future watches
      # being triggered. If isWatching is True, then
      # the future watches will be triggered.
      return isWatching