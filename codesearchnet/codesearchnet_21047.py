def many(parser):
    """Applies the parser to input zero or more times.
    
    Returns a list of parser results.
    """
    results = []
    terminate = object()
    while local_ps.value:
        result = optional(parser, terminate)
        if result == terminate:
            break
        results.append(result)
    return results