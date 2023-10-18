async def get_access_token(consumer_key, consumer_secret,
                           oauth_token, oauth_token_secret,
                           oauth_verifier, **kwargs):
    """
        get the access token of the user

    Parameters
    ----------
    consumer_key : str
        Your consumer key
    consumer_secret : str
        Your consumer secret
    oauth_token : str
        OAuth token from :func:`get_oauth_token`
    oauth_token_secret : str
        OAuth token secret from :func:`get_oauth_token`
    oauth_verifier : str
        OAuth verifier from :func:`get_oauth_verifier`

    Returns
    -------
    dict
        Access tokens
    """

    client = BasePeonyClient(consumer_key=consumer_key,
                             consumer_secret=consumer_secret,
                             access_token=oauth_token,
                             access_token_secret=oauth_token_secret,
                             api_version="",
                             suffix="")

    response = await client.api.oauth.access_token.get(
        _suffix="",
        oauth_verifier=oauth_verifier
    )

    return parse_token(response)