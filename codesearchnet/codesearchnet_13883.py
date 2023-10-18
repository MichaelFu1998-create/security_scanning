def search_images(q, start=0, size="", wait=10, asynchronous=False, cached=False):
    
    """ Returns a Google images query formatted as a GoogleSearch list object.
    """
    
    service = GOOGLE_IMAGES
    return GoogleSearch(q, start, service, size, wait, asynchronous, cached)