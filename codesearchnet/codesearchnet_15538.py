def debug_print(lst, lvl=0):
    """ Print scope tree
    args:
        lst (list): parse result
        lvl (int): current nesting level
    """
    pad = ''.join(['\t.'] * lvl)
    t = type(lst)
    if t is list:
        for p in lst:
            debug_print(p, lvl)
    elif hasattr(lst, 'tokens'):
        print(pad, t)
        debug_print(list(flatten(lst.tokens)), lvl + 1)