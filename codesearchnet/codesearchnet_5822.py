def _get_flow_for_token(csrf_token, request):
    """ Looks up the flow in session to recover information about requested
    scopes.

    Args:
        csrf_token: The token passed in the callback request that should
            match the one previously generated and stored in the request on the
            initial authorization view.

    Returns:
        The OAuth2 Flow object associated with this flow based on the
        CSRF token.
    """
    flow_pickle = request.session.get(_FLOW_KEY.format(csrf_token), None)
    return None if flow_pickle is None else jsonpickle.decode(flow_pickle)