def get_argument_starttime(self):
    """
    Helper function to get starttime argument.
    Raises exception if argument is missing.
    Returns the starttime argument.
    """
    try:
      starttime = self.get_argument(constants.PARAM_STARTTIME)
      return starttime
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)