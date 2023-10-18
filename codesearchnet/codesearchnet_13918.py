def search_images(q, start=1, count=10, wait=10, asynchronous=False, cached=False):
    
    """ Returns a Yahoo images query formatted as a YahooSearch list object.
    """
    
    service = YAHOO_IMAGES
    return YahooSearch(q, start, count, service, None, wait, asynchronous, cached)