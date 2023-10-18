def _make_flow(request, scopes, return_url=None):
    """Creates a Web Server Flow

    Args:
        request: A Django request object.
        scopes: the request oauth2 scopes.
        return_url: The URL to return to after the flow is complete. Defaults
            to the path of the current request.

    Returns:
        An OAuth2 flow object that has been stored in the session.
    """
    # Generate a CSRF token to prevent malicious requests.
    csrf_token = hashlib.sha256(os.urandom(1024)).hexdigest()

    request.session[_CSRF_KEY] = csrf_token

    state = json.dumps({
        'csrf_token': csrf_token,
        'return_url': return_url,
    })

    flow = client.OAuth2WebServerFlow(
        client_id=django_util.oauth2_settings.client_id,
        client_secret=django_util.oauth2_settings.client_secret,
        scope=scopes,
        state=state,
        redirect_uri=request.build_absolute_uri(
            urlresolvers.reverse("google_oauth:callback")))

    flow_key = _FLOW_KEY.format(csrf_token)
    request.session[flow_key] = jsonpickle.encode(flow)
    return flow