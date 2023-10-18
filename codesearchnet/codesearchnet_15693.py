def _to_json(resp):
    """
    Factors out some JSON parse code with error handling, to hopefully improve
    error messages.

    :param resp: A "requests" library response
    :return: Parsed JSON.
    :raises: InvalidJSONError If JSON parsing failed.
    """
    try:
        return resp.json()
    except ValueError as e:
        # Maybe better to report the original request URL?
        six.raise_from(InvalidJSONError(
            "Invalid JSON was received from " + resp.request.url
        ), e)