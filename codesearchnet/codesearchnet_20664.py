def search_unique(table, sample, unique_fields=None):
    """ Search for items in `table` that have the same field sub-set values as in `sample`.
    Expecting it to be unique, otherwise will raise an exception.

    Parameters
    ----------
    table: tinydb.table
    sample: dict
        Sample data

    Returns
    -------
    search_result: tinydb.database.Element
        Unique item result of the search.

    Raises
    ------
    KeyError:
        If the search returns for more than one entry.
    """
    if unique_fields is None:
        unique_fields = list(sample.keys())

    query = _query_data(sample, field_names=unique_fields, operators='__eq__')
    items = table.search(query)

    if len(items) == 1:
        return items[0]

    if len(items) == 0:
        return None

    raise MoreThanOneItemError('Expected to find zero or one items, but found '
                                '{} items.'.format(len(items)))