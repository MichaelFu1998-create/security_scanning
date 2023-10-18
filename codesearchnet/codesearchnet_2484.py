def get_required_arguments_metricnames(self):
    """
    Helper function to get metricname arguments.
    Notice that it is get_argument"s" variation, which means that this can be repeated.
    Raises exception if argument is missing.
    Returns a list of metricname arguments
    """
    try:
      metricnames = self.get_arguments(constants.PARAM_METRICNAME)
      if not metricnames:
        raise tornado.web.MissingArgumentError(constants.PARAM_METRICNAME)
      return metricnames
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)