def get_argument_query(self):
    """
    Helper function to get query argument.
    Raises exception if argument is missing.
    Returns the query argument.
    """
    try:
      query = self.get_argument(constants.PARAM_QUERY)
      return query
    except tornado.web.MissingArgumentError as e:
      raise Exception(e.log_message)