def not_found(url, wait=10):

    """ Returns True when the url generates a "404 Not Found" error.
    """

    try: connection = open(url, wait)
    except HTTP404NotFound:
        return True
    except:
        return False

    return False