def search_blogs(q, start=0, wait=10, asynchronous=False, cached=False):
    
    """ Returns a Google blogs query formatted as a GoogleSearch list object.
    """
    
    service = GOOGLE_BLOGS
    return GoogleSearch(q, start, service, "", wait, asynchronous, cached)