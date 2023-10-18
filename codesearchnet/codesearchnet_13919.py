def search_news(q, start=1, count=10, wait=10, asynchronous=False, cached=False):
    
    """ Returns a Yahoo news query formatted as a YahooSearch list object.
    """
    
    service = YAHOO_NEWS
    return YahooSearch(q, start, count, service, None, wait, asynchronous, cached)