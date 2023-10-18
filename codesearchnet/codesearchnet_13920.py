def suggest_spelling(q, wait=10, asynchronous=False, cached=False):
    
    """ Returns list of suggested spelling corrections for the given query.
    """
    
    return YahooSpelling(q, wait, asynchronous, cached)