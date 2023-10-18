def retry_auth_check(exception):
  """Specific check for auth error codes.

  Return True if we should retry.

  False otherwise.
  Args:
    exception: An exception to test for transience.

  Returns:
    True if we should retry. False otherwise.
  """
  if isinstance(exception, apiclient.errors.HttpError):
    if exception.resp.status in HTTP_AUTH_ERROR_CODES:
      _print_error('Retrying...')
      return True

  return False