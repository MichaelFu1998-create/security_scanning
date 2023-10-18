def _auth_with_refresh_token(session, refresh_token):
    """Authenticate using OAuth refresh token.

    Raises GoogleAuthError if authentication fails.

    Returns access token string.
    """
    # Make a token request.
    token_request_data = {
        'client_id': OAUTH2_CLIENT_ID,
        'client_secret': OAUTH2_CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
    }
    res = _make_token_request(session, token_request_data)
    return res['access_token']