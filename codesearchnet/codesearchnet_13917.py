def search(q, start=1, count=10, context=None, wait=10, asynchronous=False, cached=False):
    
    """ Returns a Yahoo web query formatted as a YahooSearch list object.
    """
    
    service = YAHOO_SEARCH
    return YahooSearch(q, start, count, service, context, wait, asynchronous, cached)