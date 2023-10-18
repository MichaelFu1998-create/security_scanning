def _query_data(data, field_names=None, operators='__eq__'):
    """Create a tinyDB Query object that looks for items that confirms the correspondent operator
    from `operators` for each `field_names` field values from `data`.

    Parameters
    ----------
    data: dict
        The data sample

    field_names: str or list of str
        The name of the fields in `data` that will be used for the query.

    operators: str or list of str
        A list of comparison operations for each field value in `field_names`.
        If this is a str, will use the same operator for all `field_names`.
        If you want different operators for each field, remember to use an OrderedDict for `data`.
        Check TinyDB.Query class for possible choices.

    Returns
    -------
    query: tinydb.database.Query
    """
    if field_names is None:
        field_names = list(data.keys())

    if isinstance(field_names, str):
        field_names = [field_names]

    # using OrderedDict by default, in case operators has different operators for each field.
    sample = OrderedDict([(fn, data[fn]) for fn in field_names])
    return _query_sample(sample, operators=operators)