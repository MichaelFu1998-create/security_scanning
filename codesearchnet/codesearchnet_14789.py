def get_data():
    """Returns combined list of tuples: [(table, column)].

    List is built, based on retrieved tables, where column with name
    ``tenant_id`` exists.
    """

    output = []
    tables = get_tables()
    for table in tables:
        try:
            columns = get_columns(table)
        except sa.exc.NoSuchTableError:
            continue

        for column in columns:
            if column['name'] == 'tenant_id':
                output.append((table, column))

    return output