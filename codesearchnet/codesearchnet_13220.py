def match_query(string, query):
    '''Test if a string matches a query.

    Parameters
    ----------
    string : str
        The string to test

    query : string, callable, or object
        Either a regular expression, callable function, or object.

    Returns
    -------
    match : bool
        `True` if:
        - `query` is a callable and `query(string) == True`
        - `query` is a regular expression and `re.match(query, string)`
        - or `string == query` for any other query

        `False` otherwise

    '''

    if six.callable(query):
        return query(string)

    elif (isinstance(query, six.string_types) and
          isinstance(string, six.string_types)):
        return re.match(query, string) is not None

    else:
        return query == string