def make_get_request(url, params, headers, connection):
    """
    Helper function that makes an HTTP GET request to the given firebase
    endpoint. Timeout is 60 seconds.
    `url`: The full URL of the firebase endpoint (DSN appended.)
    `params`: Python dict that is appended to the URL like a querystring.
    `headers`: Python dict. HTTP request headers.
    `connection`: Predefined HTTP connection instance. If not given, it
    is supplied by the `decorators.http_connection` function.

    The returning value is a Python dict deserialized by the JSON decoder. However,
    if the status code is not 2x or 403, an requests.HTTPError is raised.

    connection = connection_pool.get_available_connection()
    response = make_get_request('http://firebase.localhost/users', {'print': silent'},
                                {'X_FIREBASE_SOMETHING': 'Hi'}, connection)
    response => {'1': 'John Doe', '2': 'Jane Doe'}
    """
    timeout = getattr(connection, 'timeout')
    response = connection.get(url, params=params, headers=headers, timeout=timeout)
    if response.ok or response.status_code == 403:
        return response.json() if response.content else None
    else:
        response.raise_for_status()