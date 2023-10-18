def get_argument_role(self):
    """
    Helper function to get request argument.
    Raises exception if argument is missing.
    Returns the role argument.
    """
    try:
      return self.get_argument(constants.PARAM_ROLE, default=None)
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)