def _build_state_value(request_handler, user):
    """Composes the value for the 'state' parameter.

    Packs the current request URI and an XSRF token into an opaque string that
    can be passed to the authentication server via the 'state' parameter.

    Args:
        request_handler: webapp.RequestHandler, The request.
        user: google.appengine.api.users.User, The current user.

    Returns:
        The state value as a string.
    """
    uri = request_handler.request.url
    token = xsrfutil.generate_token(xsrf_secret_key(), user.user_id(),
                                    action_id=str(uri))
    return uri + ':' + token