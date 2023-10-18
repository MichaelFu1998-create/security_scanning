def _auth_with_code(session, authorization_code):
    """Authenticate using OAuth authorization code.

    Raises GoogleAuthError if authentication fails.

    Returns access token string and refresh token string.
    """
    # Make a token request.
    token_request_data = {
        'client_id': OAUTH2_CLIENT_ID,
        'client_secret': OAUTH2_CLIENT_SECRET,
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
    }
    res = _make_token_request(session, token_request_data)
    return res['access_token'], res['refresh_token']