def login(username, password, scope, client_id, client_secret, verbose):
    """
    Retrieves and stores an OAuth2 personal auth token.
    """
    if not supports_oauth():
        raise exc.TowerCLIError(
            'This version of Tower does not support OAuth2.0. Set credentials using tower-cli config.'
        )

    # Explicitly set a basic auth header for PAT acquisition (so that we don't
    # try to auth w/ an existing user+pass or oauth2 token in a config file)

    req = collections.namedtuple('req', 'headers')({})
    if client_id and client_secret:
        HTTPBasicAuth(client_id, client_secret)(req)
        req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        r = client.post(
            '/o/token/',
            data={
                "grant_type": "password",
                "username": username,
                "password": password,
                "scope": scope
            },
            headers=req.headers
        )
    elif client_id:
        req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        r = client.post(
            '/o/token/',
            data={
                "grant_type": "password",
                "username": username,
                "password": password,
                "client_id": client_id,
                "scope": scope
            },
            headers=req.headers
        )
    else:
        HTTPBasicAuth(username, password)(req)
        r = client.post(
            '/users/{}/personal_tokens/'.format(username),
            data={"description": "Tower CLI", "application": None, "scope": scope},
            headers=req.headers
        )

    if r.ok:
        result = r.json()
        result.pop('summary_fields', None)
        result.pop('related', None)
        if client_id:
            token = result.pop('access_token', None)
        else:
            token = result.pop('token', None)
        if settings.verbose:
            # only print the actual token if -v
            result['token'] = token
        secho(json.dumps(result, indent=1), fg='blue', bold=True)
        config.main(['oauth_token', token, '--scope=user'])