async def get_oauth_token(consumer_key, consumer_secret, callback_uri="oob"):
    """
    Get a temporary oauth token

    Parameters
    ----------
    consumer_key : str
        Your consumer key
    consumer_secret : str
        Your consumer secret
    callback_uri : str, optional
        Callback uri, defaults to 'oob'

    Returns
    -------
    dict
        Temporary tokens
    """

    client = BasePeonyClient(consumer_key=consumer_key,
                             consumer_secret=consumer_secret,
                             api_version="",
                             suffix="")

    response = await client.api.oauth.request_token.post(
        _suffix="",
        oauth_callback=callback_uri
    )

    return parse_token(response)