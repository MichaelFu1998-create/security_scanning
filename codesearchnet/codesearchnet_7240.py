def get_auth(credentials_prompt, refresh_token_cache, manual_login=False):
    """Authenticate with Google.

    Args:
        refresh_token_cache (RefreshTokenCache): Cache to use so subsequent
            logins may not require credentials.
        credentials_prompt (CredentialsPrompt): Prompt to use if credentials
            are required to log in.
        manual_login (bool): If true, prompt user to log in through a browser
            and enter authorization code manually. Defaults to false.

    Returns:
        dict: Google session cookies.

    Raises:
        GoogleAuthError: If authentication with Google fails.
    """
    with requests.Session() as session:
        session.headers = {'user-agent': USER_AGENT}

        try:
            logger.info('Authenticating with refresh token')
            refresh_token = refresh_token_cache.get()
            if refresh_token is None:
                raise GoogleAuthError("Refresh token not found")
            access_token = _auth_with_refresh_token(session, refresh_token)
        except GoogleAuthError as e:
            logger.info('Failed to authenticate using refresh token: %s', e)
            logger.info('Authenticating with credentials')
            if manual_login:
                authorization_code = (
                    credentials_prompt.get_authorization_code()
                )
            else:
                authorization_code = _get_authorization_code(
                    session, credentials_prompt
                )
            access_token, refresh_token = _auth_with_code(
                session, authorization_code
            )
            refresh_token_cache.set(refresh_token)

        logger.info('Authentication successful')
        return _get_session_cookies(session, access_token)