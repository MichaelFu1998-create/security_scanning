def get_scheduler_location(self, topologyName, callback=None):
    """ get scheduler location """
    isWatching = False

    # Temp dict used to return result
    # if callback is not provided.
    ret = {
        "result": None
    }
    if callback:
      isWatching = True
    else:
      def callback(data):
        """
        Custom callback to get the scheduler location right now.
        """
        ret["result"] = data

    self._get_scheduler_location_with_watch(topologyName, callback, isWatching)

    return ret["result"]