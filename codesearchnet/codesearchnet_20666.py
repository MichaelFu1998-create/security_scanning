def _query_sample(sample, operators='__eq__'):
    """Create a TinyDB query that looks for items that have each field in `sample` with a value
    compared with the correspondent operation in `operators`.

    Parameters
    ----------
    sample: dict
        The sample data

    operators: str or list of str
        A list of comparison operations for each field value in `sample`.
        If this is a str, will use the same operator for all `sample` fields.
        If you want different operators for each field, remember to use an OrderedDict for `sample`.
        Check TinyDB.Query class for possible choices.

    Returns
    -------
    query: tinydb.database.Query
    """
    if isinstance(operators, str):
        operators = [operators] * len(sample)

    if len(sample) != len(operators):
        raise ValueError('Expected `operators` to be a string or a list with the same'
                         ' length as `field_names` ({}), got {}.'.format(len(sample),
                                                                         operators))

    queries = []
    for i, fn in enumerate(sample):
        fv = sample[fn]
        op = operators[i]
        queries.append(_build_query(field_name=fn,
                                    field_value=fv,
                                    operator=op))

    return _concat_queries(queries, operators='__and__')