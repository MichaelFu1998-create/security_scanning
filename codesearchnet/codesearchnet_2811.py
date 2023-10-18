def set_config(self, config):
    """Set topology-wide configuration to the topology

    :type config: dict
    :param config: topology-wide config
    """
    if not isinstance(config, dict):
      raise TypeError("Argument to set_config needs to be dict, given: %s" % str(config))
    self._topology_config = config