def get_topologies(self, callback=None):
    """ get topologies """
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
        """Custom callback to get the topologies right now."""
        ret["result"] = data

    try:
      # Ensure the topology path exists. If a topology has never been deployed
      # then the path will not exist so create it and don't crash.
      # (fixme) add a watch instead of creating the path?
      self.client.ensure_path(self.get_topologies_path())

      self._get_topologies_with_watch(callback, isWatching)
    except NoNodeError:
      self.client.stop()
      path = self.get_topologies_path()
      raise_(StateException("Error required topology path '%s' not found" % (path),
                            StateException.EX_TYPE_NO_NODE_ERROR), sys.exc_info()[2])

    # The topologies are now populated with the data.
    return ret["result"]