def normalize_query(query_string, terms=TERMS, norm_space=NORM_SPACE):
    """
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
    ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    """
    return [
        norm_space(' ', (t[0] or t[1]).strip()) for t in terms(query_string)]