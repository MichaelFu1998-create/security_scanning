def get_argument_instance(self):
    """
    Helper function to get instance argument.
    Raises exception if argument is missing.
    Returns the instance argument.
    """
    try:
      instance = self.get_argument(constants.PARAM_INSTANCE)
      return instance
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)