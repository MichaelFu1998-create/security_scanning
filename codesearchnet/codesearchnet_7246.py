def _get_session_cookies(session, access_token):
    """Use the access token to get session cookies.

    Raises GoogleAuthError if session cookies could not be loaded.

    Returns dict of cookies.
    """
    headers = {'Authorization': 'Bearer {}'.format(access_token)}

    try:
        r = session.get(('https://accounts.google.com/accounts/OAuthLogin'
                         '?source=hangups&issueuberauth=1'), headers=headers)
        r.raise_for_status()
    except requests.RequestException as e:
        raise GoogleAuthError('OAuthLogin request failed: {}'.format(e))
    uberauth = r.text

    try:
        r = session.get(('https://accounts.google.com/MergeSession?'
                         'service=mail&'
                         'continue=http://www.google.com&uberauth={}')
                        .format(uberauth), headers=headers)
        r.raise_for_status()
    except requests.RequestException as e:
        raise GoogleAuthError('MergeSession request failed: {}'.format(e))

    cookies = session.cookies.get_dict(domain='.google.com')
    if cookies == {}:
        raise GoogleAuthError('Failed to find session cookies')
    return cookies