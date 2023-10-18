async def github_request(session, api_token,
                         query=None, mutation=None, variables=None):
    """Send a request to the GitHub v4 (GraphQL) API.

    The request is asynchronous, with asyncio.

    Parameters
    ----------
    session : `aiohttp.ClientSession`
        Your application's aiohttp client session.
    api_token : `str`
        A GitHub personal API token. See the `GitHub personal access token
        guide`_.
    query : `str` or `GitHubQuery`
        GraphQL query string. If provided, then the ``mutation`` parameter
        should not be set. For examples, see the `GitHub guide to query and
        mutation operations`_.
    mutation : `str` or `GitHubQuery`
        GraphQL mutation string. If provided, then the ``query`` parameter
        should not be set. For examples, see the `GitHub guide to query and
        mutation operations`_.
    variables : `dict`
        GraphQL variables, as a JSON-compatible dictionary. This is only
        required if the ``query`` or ``mutation`` uses GraphQL variables.

    Returns
    -------
    data : `dict`
        Parsed JSON as a `dict` object.

    .. `GitHub personal access token guide`: https://ls.st/41d
    .. `GitHub guide to query and mutation operations`: https://ls.st/9s7
    """
    payload = {}
    if query is not None:
        payload['query'] = str(query)  # converts a GitHubQuery
    if mutation is not None:
        payload['mutation'] = str(mutation)  # converts a GitHubQuery
    if variables is not None:
        payload['variables'] = variables

    headers = {'Authorization': 'token {}'.format(api_token)}

    url = 'https://api.github.com/graphql'
    async with session.post(url, json=payload, headers=headers) as response:
        data = await response.json()

    return data