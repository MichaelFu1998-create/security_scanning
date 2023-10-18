def _get_topology_with_watch(self, topologyName, callback, isWatching):
    """
    Helper function to get pplan with
    a callback. The future watch is placed
    only if isWatching is True.
    """
    path = self.get_topology_path(topologyName)
    if isWatching:
      LOG.info("Adding data watch for path: " + path)

    # pylint: disable=unused-variable, unused-argument
    @self.client.DataWatch(path)
    def watch_topology(data, stats):
      """ watch topology """
      if data:
        topology = Topology()
        topology.ParseFromString(data)
        callback(topology)
      else:
        callback(None)

      # Returning False will result in no future watches
      # being triggered. If isWatching is True, then
      # the future watches will be triggered.
      return isWatching