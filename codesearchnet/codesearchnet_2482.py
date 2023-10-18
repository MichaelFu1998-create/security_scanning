def get_argument_offset(self):
    """
    Helper function to get offset argument.
    Raises exception if argument is missing.
    Returns the offset argument.
    """
    try:
      offset = self.get_argument(constants.PARAM_OFFSET)
      return offset
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)