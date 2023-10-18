def search(q, start=0, wait=10, asynchronous=False, cached=False):
    
    """ Returns a Google web query formatted as a GoogleSearch list object.
    """
    
    service = GOOGLE_SEARCH
    return GoogleSearch(q, start, service, "", wait, asynchronous, cached)