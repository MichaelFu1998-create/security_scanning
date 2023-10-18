def seq(*sequence):
    """Runs a series of parsers in sequence optionally storing results in a returned dictionary.
    
    For example:
    seq(whitespace, ('phone', digits), whitespace, ('name', remaining))
    """
    results = {}
    for p in sequence:
        if callable(p): 
            p()
            continue
        k, v = p
        results[k] = v()
    return results