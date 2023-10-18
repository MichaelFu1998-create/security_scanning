def make_delete_request(url, params, headers, connection):
    """
    Helper function that makes an HTTP DELETE request to the given firebase
    endpoint. Timeout is 60 seconds.
    `url`: The full URL of the firebase endpoint (DSN appended.)
    `params`: Python dict that is appended to the URL like a querystring.
    `headers`: Python dict. HTTP request headers.
    `connection`: Predefined HTTP connection instance. If not given, it
    is supplied by the `decorators.http_connection` function.

    The returning value is NULL. However, if the status code is not 2x or 403,
    an requests.HTTPError is raised.

    connection = connection_pool.get_available_connection()
    response = make_put_request('http://firebase.localhost/users/1',
                                {'X_FIREBASE_SOMETHING': 'Hi'}, connection)
    response => NULL or {'error': 'Permission denied.'}
    """
    timeout = getattr(connection, 'timeout')
    response = connection.delete(url, params=params, headers=headers, timeout=timeout)
    if response.ok or response.status_code == 403:
        return response.json() if response.content else None
    else:
        response.raise_for_status()