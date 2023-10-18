def get_argument_cluster(self):
    """
    Helper function to get request argument.
    Raises exception if argument is missing.
    Returns the cluster argument.
    """
    try:
      return self.get_argument(constants.PARAM_CLUSTER)
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)