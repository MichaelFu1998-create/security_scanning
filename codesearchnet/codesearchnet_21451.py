def count(cls, cur, table:str, where_keys: list=None):
        """
        gives the number of records in the table

        Args:
            table: a string indicating the name of the table

        Returns:
            an integer indicating the number of records in the table

        """

        if where_keys:
            where_clause, values = cls._get_where_clause_with_values(where_keys)
            query = cls._count_query_where.format(table, where_clause)
            q, t = query, values
        else:
            query = cls._count_query.format(table)
            q, t = query, ()
        yield from cur.execute(q, t)
        result = yield from cur.fetchone()
        return int(result[0])