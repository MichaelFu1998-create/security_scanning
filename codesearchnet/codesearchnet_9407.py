def retry_api_check(exception):
  """Return True if we should retry. False otherwise.

  Args:
    exception: An exception to test for transience.

  Returns:
    True if we should retry. False otherwise.
  """
  if isinstance(exception, apiclient.errors.HttpError):
    if exception.resp.status in TRANSIENT_HTTP_ERROR_CODES:
      _print_error('Retrying...')
      return True

  if isinstance(exception, socket.error):
    if exception.errno in TRANSIENT_SOCKET_ERROR_CODES:
      _print_error('Retrying...')
      return True

  if isinstance(exception, oauth2client.client.AccessTokenRefreshError):
    _print_error('Retrying...')
    return True

  # For a given installation, this could be a permanent error, but has only
  # been observed as transient.
  if isinstance(exception, SSLError):
    _print_error('Retrying...')
    return True

  # This has been observed as a transient error:
  #   ServerNotFoundError: Unable to find the server at genomics.googleapis.com
  if isinstance(exception, ServerNotFoundError):
    _print_error('Retrying...')
    return True

  return False