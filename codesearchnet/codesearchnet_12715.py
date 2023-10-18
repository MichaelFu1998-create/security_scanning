async def async_oauth_dance(consumer_key, consumer_secret, callback_uri="oob"):
    """
        OAuth dance to get the user's access token

    Parameters
    ----------
    consumer_key : str
        Your consumer key
    consumer_secret : str
        Your consumer secret
    callback_uri : str
        Callback uri, defaults to 'oob'

    Returns
    -------
    dict
        Access tokens
    """

    token = await get_oauth_token(consumer_key, consumer_secret, callback_uri)

    oauth_verifier = await get_oauth_verifier(token['oauth_token'])

    token = await get_access_token(
        consumer_key,
        consumer_secret,
        oauth_verifier=oauth_verifier,
        **token
    )

    token = dict(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=token['oauth_token'],
        access_token_secret=token['oauth_token_secret']
    )

    return token