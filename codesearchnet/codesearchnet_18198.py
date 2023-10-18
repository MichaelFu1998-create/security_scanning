def create_txacme_client_creator(key, reactor, url, alg=RS256):
    """
    Create a creator for txacme clients to provide to the txacme service. See
    ``txacme.client.Client.from_url()``. We create the underlying JWSClient
    with a non-persistent pool to avoid
    https://github.com/mithrandi/txacme/issues/86.

    :return: a callable that returns a deffered that returns the client
    """
    # Creating an Agent without specifying a pool gives us the default pool
    # which is non-persistent.
    jws_client = JWSClient(HTTPClient(agent=Agent(reactor)), key, alg)

    return partial(txacme_Client.from_url, reactor, url, key, alg, jws_client)