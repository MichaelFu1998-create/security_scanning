def oauth2_dance(consumer_key, consumer_secret, loop=None):
    """
        oauth2 dance

    Parameters
    ----------
    consumer_key : str
        Your consumer key
    consumer_secret : str
        Your consumer secret
    loop : event loop, optional
        event loop to use

    Returns
    -------
    str
        Bearer token
    """
    loop = asyncio.get_event_loop() if loop is None else loop
    client = BasePeonyClient(consumer_key=consumer_key,
                             consumer_secret=consumer_secret,
                             auth=oauth.OAuth2Headers)

    loop.run_until_complete(client.headers.sign())
    return client.headers.token