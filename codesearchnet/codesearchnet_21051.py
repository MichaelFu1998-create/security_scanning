def string(string):
    """Iterates over string, matching input to the items provided.
    
    The most obvious usage of this is to accept an entire string of characters,
    However this is function is more general than that. It takes an iterable
    and for each item, it tries one_of for that set. For example, 
       string(['aA','bB','cC'])
    will accept 'abc' in either case. 
    
    note, If you wish to match caseless strings as in the example, use 
    picoparse.text.caseless_string.
    """
    found = []
    for c in string:
        found.append(one_of(c))
    return found