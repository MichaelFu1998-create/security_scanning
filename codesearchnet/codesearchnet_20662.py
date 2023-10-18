def insert_unique(table, data, unique_fields=None, *, raise_if_found=False):
    """Insert `data` into `table` ensuring that data has unique values
    in `table` for the fields listed in `unique_fields`.

    If `raise_if_found` is True, will raise an NotUniqueItemError if
    another item with the same `unique_fields` values are found
    previously in `table`.
    If False, will return the `eid` from the item found.

    Parameters
    ----------
    table: tinydb.Table

    data: dict

    unique_fields: list of str
        Name of fields (keys) from `data` which are going to be used to build
        a sample to look for exactly the same values in the database.
        If None, will use every key in `data`.

    raise_if_found: bool

    Returns
    -------
    eid: int
        Id of the object inserted or the one found with same `unique_fields`.

    Raises
    ------
    MoreThanOneItemError
        Raise even with `raise_with_found` == False if it finds more than one item
        with the same values as the sample.

    NotUniqueItemError
        If `raise_if_found` is True and an item with the same `unique_fields`
        values from `data` is found in `table`.
    """
    item = find_unique(table, data, unique_fields)
    if item is not None:
        if raise_if_found:
            raise NotUniqueItemError('Not expected to find an item with the same '
                                     'values for {}. Inserting {} got {} in eid {}.'.format(unique_fields,
                                                                                            data,
                                                                                            table.get(eid=item),
                                                                                            item))
        else:
            return item

    return table.insert(data)