def is_type(url, types=[], wait=10):

    """ Determine the MIME-type of the document behind the url.

    MIME is more reliable than simply checking the document extension.
    Returns True when the MIME-type starts with anything in the list of types.

    """

    # Types can also be a single string for convenience.
    if isinstance(types, str):
        types = [types]

    try: connection = open(url, wait)
    except:
        return False

    type = connection.info()["Content-Type"]
    for t in types:
        if type.startswith(t): return True

    return False