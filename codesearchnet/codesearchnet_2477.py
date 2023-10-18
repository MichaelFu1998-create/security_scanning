def get_argument_component(self):
    """
    Helper function to get component argument.
    Raises exception if argument is missing.
    Returns the component argument.
    """
    try:
      component = self.get_argument(constants.PARAM_COMPONENT)
      return component
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)