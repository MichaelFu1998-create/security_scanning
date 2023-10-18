def many_until(these, term):
    """Consumes as many of these as it can until it term is encountered.
    
    Returns a tuple of the list of these results and the term result 
    """
    results = []
    while True:
        stop, result = choice(_tag(True, term),
                              _tag(False, these))
        if stop:
            return results, result
        else:
            results.append(result)