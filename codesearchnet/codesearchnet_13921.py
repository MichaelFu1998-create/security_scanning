def sort(words, context="", strict=True, relative=True, service=YAHOO_SEARCH,
         wait=10, asynchronous=False, cached=False):
    
    """Performs a Yahoo sort on the given list.
    
    Sorts the items in the list according to 
    the result count Yahoo yields on an item.
    
    Setting a context sorts the items according
    to their relation to this context;
    for example sorting [red, green, blue] by "love"
    yields red as the highest results,
    likely because red is the color commonly associated with love.
    
    """
    
    results = []
    for word in words:
        q = word + " " + context
        q.strip()
        if strict: q = "\""+q+"\""
        r = YahooSearch(q, 1, 1, service, context, wait, asynchronous, cached)
        results.append(r)
        
    results.sort(YahooResults.__cmp__)
    results.reverse()
    
    if relative and len(results) > 0:
        sum = 0.000000000000000001
        for r in results: sum += r.total
        for r in results: r.total /= float(sum)
    
    results = [(r.query, r.total) for r in results]
    return results