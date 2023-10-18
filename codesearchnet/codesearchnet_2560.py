def _get_packing_plan_with_watch(self, topologyName, callback, isWatching):
    """
    Helper function to get packing_plan with
    a callback. The future watch is placed
    only if isWatching is True.
    """
    path = self.get_packing_plan_path(topologyName)
    if isWatching:
      LOG.info("Adding data watch for path: " + path)

    # pylint: disable=unused-argument,unused-variable
    @self.client.DataWatch(path)
    def watch_packing_plan(data, stats):
      """ watch the packing plan for updates """
      if data:
        packing_plan = PackingPlan()
        packing_plan.ParseFromString(data)
        callback(packing_plan)
      else:
        callback(None)

      # Returning False will result in no future watches
      # being triggered. If isWatching is True, then
      # the future watches will be triggered.
      return isWatching