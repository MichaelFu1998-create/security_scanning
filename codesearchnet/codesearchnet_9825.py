def _distribution(gtfs, table, column):
    """Count occurrences of values AND return it as a string.

    Example return value:   '1:5 2:15'"""
    cur = gtfs.conn.cursor()
    cur.execute('SELECT {column}, count(*) '
                'FROM {table} GROUP BY {column} '
                'ORDER BY {column}'.format(column=column, table=table))
    return ' '.join('%s:%s' % (t, c) for t, c in cur)