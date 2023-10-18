def _request(self, method, *relative_path_parts, **kwargs):
    """Sends an HTTP request to the REST API and receives the requested data.

    :param str method: HTTP method name
    :param relative_path_parts: the relative paths for the request URI
    :param kwargs: argument keywords
    :returns: requested data
    :raises APIError: for non-2xx responses

    """
    uri = self._create_api_uri(*relative_path_parts)
    if method == 'get':
      response = get(uri, auth=self.auth, params=kwargs.get('params', None))
    elif method == 'post':
      response = post(uri, auth=self.auth, json=kwargs.get('data', None))
    else:
      response = delete(uri, auth=self.auth, json=kwargs.get('data', None))
    return self._handle_response(response).json()