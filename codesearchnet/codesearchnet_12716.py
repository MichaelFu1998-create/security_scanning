def parse_token(response):
    """
    parse the responses containing the tokens

    Parameters
    ----------
    response : str
        The response containing the tokens

    Returns
    -------
    dict
        The parsed tokens
    """
    items = response.split("&")
    items = [item.split("=") for item in items]

    return {key: value for key, value in items}