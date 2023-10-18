def _retry_storage_check(exception):
  """Return True if we should retry, False otherwise."""
  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
  print_error(
      '%s: Exception %s: %s' % (now, type(exception).__name__, str(exception)))
  return isinstance(exception, oauth2client.client.AccessTokenRefreshError)