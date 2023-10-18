def execute(cur, *args):
    """Utility function to print sqlite queries before executing.

    Use instead of cur.execute().  First argument is cursor.

    cur.execute(stmt)
    becomes
    util.execute(cur, stmt)
    """
    stmt = args[0]
    if len(args) > 1:
        stmt = stmt.replace('%', '%%').replace('?', '%r')
        print(stmt % (args[1]))
    return cur.execute(*args)