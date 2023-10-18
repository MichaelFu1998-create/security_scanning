def raw_sql(cls, cur, query: str, values: tuple):
        """
        Run a raw sql query

        Args:
            query : query string to execute
            values : tuple of values to be used with the query

        Returns:
            result of query as list of named tuple

        """
        yield from cur.execute(query, values)
        return (yield from cur.fetchall())