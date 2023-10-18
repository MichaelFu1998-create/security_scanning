def schema(tg):
    """
    Convert the table and column descriptions of a `TableGroup` into specifications for the
    DB schema.

    :param ds:
    :return: A pair (tables, reference_tables).
    """
    tables = {}
    for tname, table in tg.tabledict.items():
        t = TableSpec.from_table_metadata(table)
        tables[t.name] = t
        for at in t.many_to_many.values():
            tables[at.name] = at

    # We must determine the order in which tables must be created!
    ordered = OrderedDict()
    i = 0

    # We loop through the tables repeatedly, and whenever we find one, which has all
    # referenced tables already in ordered, we move it from tables to ordered.
    while tables and i < 100:
        i += 1
        for table in list(tables.keys()):
            if all((ref[1] in ordered) or ref[1] == table for ref in tables[table].foreign_keys):
                # All referenced tables are already created (or self-referential).
                ordered[table] = tables.pop(table)
                break
    if tables:  # pragma: no cover
        raise ValueError('there seem to be cyclic dependencies between the tables')

    return list(ordered.values())