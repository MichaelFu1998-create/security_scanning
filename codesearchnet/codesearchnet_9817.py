def copy(cls, conn, **where):
        """Copy data from one table to another while filtering data at the same time

        Parameters
        ----------
        conn: sqlite3 DB connection.  It must have a second database
            attached as "other".
        **where : keyword arguments
            specifying (start_ut and end_ut for filtering, see the copy_where clause in the subclasses)
        """
        cur = conn.cursor()
        if where and cls.copy_where:
            copy_where = cls.copy_where.format(**where)
            # print(copy_where)
        else:
            copy_where = ''
        cur.execute('INSERT INTO %s '
                    'SELECT * FROM source.%s %s' % (cls.table, cls.table, copy_where))