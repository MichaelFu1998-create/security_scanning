def oauth_dance(consumer_key, consumer_secret,
                oauth_callback="oob", loop=None):
    """
        OAuth dance to get the user's access token

    It calls async_oauth_dance and create event loop of not given

    Parameters
    ----------
    consumer_key : str
        Your consumer key
    consumer_secret : str
        Your consumer secret
    oauth_callback : str
        Callback uri, defaults to 'oob'
    loop : event loop
        asyncio event loop

    Returns
    -------
    dict
        Access tokens
    """
    loop = asyncio.get_event_loop() if loop is None else loop

    coro = async_oauth_dance(consumer_key, consumer_secret, oauth_callback)
    return loop.run_until_complete(coro)