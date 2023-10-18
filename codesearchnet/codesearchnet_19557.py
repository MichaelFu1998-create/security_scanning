def get_insert_query(table, fields=None, field_count=None):
    """
    format insert query
    :param table: str
    :param fields: list[str]
    :param field_count: int
    :return: str
    """
    if fields:
        q = 'insert into %s ({0}) values ({1});' % table
        l = len(fields)
        q = q.format(','.join(fields), ','.join(['%s'] * l))
    elif field_count:
        q = 'insert into %s values ({0});' % table
        q = q.format(','.join(['%s'] * field_count))
    else:
        raise ValueError('fields or field_count need')

    return q