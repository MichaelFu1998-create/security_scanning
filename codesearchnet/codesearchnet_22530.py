def _handle_response(self, response):
    """Returns the given response or raises an APIError for non-2xx responses.

    :param requests.Response response: HTTP response
    :returns: requested data
    :rtype: requests.Response
    :raises APIError: for non-2xx responses

    """
    if not str(response.status_code).startswith('2'):
      raise get_api_error(response)
    return response