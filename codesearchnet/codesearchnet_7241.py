def get_auth_stdin(refresh_token_filename, manual_login=False):
    """Simple wrapper for :func:`get_auth` that prompts the user using stdin.

    Args:
        refresh_token_filename (str): Path to file where refresh token will be
            cached.
        manual_login (bool): If true, prompt user to log in through a browser
            and enter authorization code manually. Defaults to false.

    Raises:
        GoogleAuthError: If authentication with Google fails.
    """
    refresh_token_cache = RefreshTokenCache(refresh_token_filename)
    return get_auth(
        CredentialsPrompt(), refresh_token_cache, manual_login=manual_login
    )