def get_argument_endtime(self):
    """
    Helper function to get endtime argument.
    Raises exception if argument is missing.
    Returns the endtime argument.
    """
    try:
      endtime = self.get_argument(constants.PARAM_ENDTIME)
      return endtime
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)