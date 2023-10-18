def get_argument_environ(self):
    """
    Helper function to get request argument.
    Raises exception if argument is missing.
    Returns the environ argument.
    """
    try:
      return self.get_argument(constants.PARAM_ENVIRON)
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)