def search_news(q, start=0, wait=10, asynchronous=False, cached=False):
    
    """ Returns a Google news query formatted as a GoogleSearch list object.
    """
    
    service = GOOGLE_NEWS
    return GoogleSearch(q, start, service, "", wait, asynchronous, cached)