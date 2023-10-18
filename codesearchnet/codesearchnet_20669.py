def _build_query(field_name, field_value, operator='__eq__'):
    """Create a tinyDB Query object with the format:
    (where(`field_name`) `operator` `field_value`)

    Parameters
    ----------
    field_name: str
        The name of the field to be queried.

    field_value:
        The value of the field

    operator: str
        The comparison operator.
        Check TinyDB.Query class for possible choices.

    Returns
    -------
    query: tinydb.database.Query
    """
    qelem = where(field_name)

    if not hasattr(qelem, operator):
        raise NotImplementedError('Operator `{}` not found in query object.'.format(operator))
    else:
        query = getattr(qelem, operator)

    return query(field_value)