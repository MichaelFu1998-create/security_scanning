def _get_topologies_with_watch(self, callback, isWatching):
    """
    Helper function to get topologies with
    a callback. The future watch is placed
    only if isWatching is True.
    """
    path = self.get_topologies_path()
    if isWatching:
      LOG.info("Adding children watch for path: " + path)

    # pylint: disable=unused-variable
    @self.client.ChildrenWatch(path)
    def watch_topologies(topologies):
      """ callback to watch topologies """
      callback(topologies)

      # Returning False will result in no future watches
      # being triggered. If isWatching is True, then
      # the future watches will be triggered.
      return isWatching