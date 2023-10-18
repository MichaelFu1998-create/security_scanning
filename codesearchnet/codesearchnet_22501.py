def get_api_error(response):
  """Acquires the correct error for a given response.

  :param requests.Response response: HTTP error response
  :returns: the appropriate error for a given response
  :rtype: APIError

  """
  error_class = _status_code_to_class.get(response.status_code, APIError)
  return error_class(response)