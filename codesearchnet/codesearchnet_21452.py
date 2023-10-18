def insert(cls, cur, table: str, values: dict):
        """
        Creates an insert statement with only chosen fields

        Args:
            table: a string indicating the name of the table
            values: a dict of fields and values to be inserted

        Returns:
            A 'Record' object with table columns as properties

        """
        keys = cls._COMMA.join(values.keys())
        value_place_holder = cls._PLACEHOLDER * len(values)
        query = cls._insert_string.format(table, keys, value_place_holder[:-1])
        yield from cur.execute(query, tuple(values.values()))
        return (yield from cur.fetchone())