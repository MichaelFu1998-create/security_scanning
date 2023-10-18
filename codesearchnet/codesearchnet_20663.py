def search_sample(table, sample):
    """Search for items in `table` that have the same field sub-set values as in `sample`.

    Parameters
    ----------
    table: tinydb.table

    sample: dict
        Sample data

    Returns
    -------
    search_result: list of dict
        List of the items found. The list is empty if no item is found.
    """
    query = _query_sample(sample=sample, operators='__eq__')

    return table.search(query)