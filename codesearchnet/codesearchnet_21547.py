def get_installation_token(installation_id, integration_jwt):
    """Create a GitHub token for an integration installation.

    Parameters
    ----------
    installation_id : `int`
        Installation ID. This is available in the URL of the integration's
        **installation** ID.
    integration_jwt : `bytes`
        The integration's JSON Web Token (JWT). You can create this with
        `create_jwt`.

    Returns
    -------
    token_obj : `dict`
        GitHub token object. Includes the fields:

        - ``token``: the token string itself.
        - ``expires_at``: date time string when the token expires.

    Example
    -------
    The typical workflow for authenticating to an integration installation is:

    .. code-block:: python

       from dochubadapter.github import auth
       jwt = auth.create_jwt(integration_id, private_key_path)
       token_obj = auth.get_installation_token(installation_id, jwt)
       print(token_obj['token'])

    Notes
    -----
    See
    https://developer.github.com/early-access/integrations/authentication/#as-an-installation
    for more information
    """
    api_root = 'https://api.github.com'
    url = '{root}/installations/{id_:d}/access_tokens'.format(
        api_root=api_root,
        id_=installation_id)

    headers = {
        'Authorization': 'Bearer {0}'.format(integration_jwt.decode('utf-8')),
        'Accept': 'application/vnd.github.machine-man-preview+json'
    }

    resp = requests.post(url, headers=headers)
    resp.raise_for_status()
    return resp.json()