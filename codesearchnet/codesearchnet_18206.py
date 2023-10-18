def raise_for_status(response):
    """
    Raises a `requests.exceptions.HTTPError` if the response did not succeed.
    Adapted from the Requests library:
    https://github.com/kennethreitz/requests/blob/v2.8.1/requests/models.py#L825-L837
    """
    http_error_msg = ''

    if 400 <= response.code < 500:
        http_error_msg = '%s Client Error for url: %s' % (
            response.code, uridecode(response.request.absoluteURI))

    elif 500 <= response.code < 600:
        http_error_msg = '%s Server Error for url: %s' % (
            response.code, uridecode(response.request.absoluteURI))

    if http_error_msg:
        raise HTTPError(http_error_msg, response=response)

    return response