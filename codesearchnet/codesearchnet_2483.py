def get_argument_length(self):
    """
    Helper function to get length argument.
    Raises exception if argument is missing.
    Returns the length argument.
    """
    try:
      length = self.get_argument(constants.PARAM_LENGTH)
      return length
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)