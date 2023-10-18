def _concat_queries(queries, operators='__and__'):
    """Create a tinyDB Query object that is the concatenation of each query in `queries`.
    The concatenation operator is taken from `operators`.

    Parameters
    ----------
    queries: list of tinydb.Query
        The list of tinydb.Query to be joined.

    operators: str or list of str
        List of binary operators to join `queries` into one query.
        Check TinyDB.Query class for possible choices.

    Returns
    -------
    query: tinydb.database.Query
    """
    # checks first
    if not queries:
        raise ValueError('Expected some `queries`, got {}.'.format(queries))

    if len(queries) == 1:
        return queries[0]

    if isinstance(operators, str):
        operators = [operators] * (len(queries) - 1)

    if len(queries) - 1 != len(operators):
        raise ValueError('Expected `operators` to be a string or a list with the same'
                         ' length as `field_names` ({}), got {}.'.format(len(queries),
                                                                         operators))

    # recursively build the query
    first, rest, end = queries[0], queries[1:-1], queries[-1:][0]
    bigop = getattr(first, operators[0])
    for i, q in enumerate(rest):
        bigop = getattr(bigop(q), operators[i])

    return bigop(end)