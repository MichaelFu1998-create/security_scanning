def _get_flow_for_token(csrf_token):
    """Retrieves the flow instance associated with a given CSRF token from
    the Flask session."""
    flow_pickle = session.pop(
        _FLOW_KEY.format(csrf_token), None)

    if flow_pickle is None:
        return None
    else:
        return pickle.loads(flow_pickle)