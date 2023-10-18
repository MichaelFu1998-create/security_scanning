def reverse_guard(lst):
    """ Reverse guard expression. not
        (@a > 5) ->  (@a =< 5)
    Args:
        lst (list): Expression
    returns:
        list
    """
    rev = {'<': '>=', '>': '=<', '>=': '<', '=<': '>'}
    return [rev[l] if l in rev else l for l in lst]