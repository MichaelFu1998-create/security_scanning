def _make_token_request(session, token_request_data):
    """Make OAuth token request.

    Raises GoogleAuthError if authentication fails.

    Returns dict response.
    """
    try:
        r = session.post(OAUTH2_TOKEN_REQUEST_URL, data=token_request_data)
        r.raise_for_status()
    except requests.RequestException as e:
        raise GoogleAuthError('Token request failed: {}'.format(e))
    else:
        res = r.json()
        # If an error occurred, a key 'error' will contain an error code.
        if 'error' in res:
            raise GoogleAuthError(
                'Token request error: {!r}'.format(res['error'])
            )
        return res