def get_argument_topology(self):
    """
    Helper function to get topology argument.
    Raises exception if argument is missing.
    Returns the topology argument.
    """
    try:
      topology = self.get_argument(constants.PARAM_TOPOLOGY)
      return topology
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)