def _get_execution_state_with_watch(self, topologyName, callback, isWatching):
    """
    Helper function to get execution state with
    a callback. The future watch is placed
    only if isWatching is True.
    """
    path = self.get_execution_state_path(topologyName)
    if isWatching:
      LOG.info("Adding data watch for path: " + path)

    # pylint: disable=unused-variable, unused-argument
    @self.client.DataWatch(path)
    def watch_execution_state(data, stats):
      """ invoke callback to watch execute state """
      if data:
        executionState = ExecutionState()
        executionState.ParseFromString(data)
        callback(executionState)
      else:
        callback(None)

      # Returning False will result in no future watches
      # being triggered. If isWatching is True, then
      # the future watches will be triggered.
      return isWatching