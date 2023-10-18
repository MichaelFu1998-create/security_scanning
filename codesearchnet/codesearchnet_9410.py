def execute(api):
    """Executes operation.

    Args:
      api: The base API object

    Returns:
       A response body object
    """
    try:
      return api.execute()
    except Exception as exception:
      now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
      _print_error('%s: Exception %s: %s' % (now, type(exception).__name__,
                                             str(exception)))
      # Re-raise exception to be handled by retry logic
      raise exception