def get_tmaster(self, topologyName, callback=None):
    """ get tmaster """
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
        Custom callback to get the topologies right now.
        """
        ret["result"] = data

    self._get_tmaster_with_watch(topologyName, callback, isWatching)

    # The topologies are now populated with the data.
    return ret["result"]