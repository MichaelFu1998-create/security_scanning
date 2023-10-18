def _parse_state_value(state, user):
    """Parse the value of the 'state' parameter.

    Parses the value and validates the XSRF token in the state parameter.

    Args:
        state: string, The value of the state parameter.
        user: google.appengine.api.users.User, The current user.

    Returns:
        The redirect URI, or None if XSRF token is not valid.
    """
    uri, token = state.rsplit(':', 1)
    if xsrfutil.validate_token(xsrf_secret_key(), token, user.user_id(),
                               action_id=uri):
        return uri
    else:
        return None