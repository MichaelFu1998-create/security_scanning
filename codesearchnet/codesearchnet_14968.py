def max_parameter_substitution():
    """
    SQLite has a limit on the max number of variables allowed for parameter substitution. This limit is usually 999, but
    can be compiled to a different number. This function calculates what the max is for the sqlite version running on the device.
    We use the calculated value to chunk our SQL bulk insert statements when deserializing from the store to the app layer.
    """
    if os.path.isfile(SQLITE_VARIABLE_FILE_CACHE):
        return
    conn = sqlite3.connect(':memory:')
    low = 1
    high = 1000  # hard limit for SQLITE_MAX_VARIABLE_NUMBER <http://www.sqlite.org/limits.html>
    conn.execute('CREATE TABLE T1 (id C1)')
    while low < high - 1:
        guess = (low + high) // 2
        try:
            statement = 'select * from T1 where id in (%s)' % ','.join(['?' for _ in range(guess)])
            values = [i for i in range(guess)]
            conn.execute(statement, values)
        except sqlite3.DatabaseError as ex:
            if 'too many SQL variables' in str(ex):
                high = guess
            else:
                raise
        else:
            low = guess
    conn.close()
    with open(SQLITE_VARIABLE_FILE_CACHE, 'w') as file:
        file.write(str(low))