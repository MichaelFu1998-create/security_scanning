def _get_scheduler_location_with_watch(self, topologyName, callback, isWatching):
    """
    Helper function to get scheduler location with
    a callback. The future watch is placed
    only if isWatching is True.
    """
    path = self.get_scheduler_location_path(topologyName)
    if isWatching:
      LOG.info("Adding data watch for path: " + path)

    # pylint: disable=unused-variable, unused-argument
    @self.client.DataWatch(path)
    def watch_scheduler_location(data, stats):
      """ invoke callback to watch scheduler location """
      if data:
        scheduler_location = SchedulerLocation()
        scheduler_location.ParseFromString(data)
        callback(scheduler_location)
      else:
        callback(None)

      # Returning False will result in no future watches
      # being triggered. If isWatching is True, then
      # the future watches will be triggered.
      return isWatching