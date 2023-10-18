def _parse_exchange_token_response(content):
    """Parses response of an exchange token request.

    Most providers return JSON but some (e.g. Facebook) return a
    url-encoded string.

    Args:
        content: The body of a response

    Returns:
        Content as a dictionary object. Note that the dict could be empty,
        i.e. {}. That basically indicates a failure.
    """
    resp = {}
    content = _helpers._from_bytes(content)
    try:
        resp = json.loads(content)
    except Exception:
        # different JSON libs raise different exceptions,
        # so we just do a catch-all here
        resp = _helpers.parse_unique_urlencoded(content)

    # some providers respond with 'expires', others with 'expires_in'
    if resp and 'expires' in resp:
        resp['expires_in'] = resp.pop('expires')

    return resp