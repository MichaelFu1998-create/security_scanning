def update(cls, cur, table: str, values: dict, where_keys: list) -> tuple:
        """
        Creates an update query with only chosen fields
        Supports only a single field where clause

        Args:
            table: a string indicating the name of the table
            values: a dict of fields and values to be inserted
            where_keys: list of dictionary
            example of where keys: [{'name':('>', 'cip'),'url':('=', 'cip.com'},{'type':{'<=', 'manufacturer'}}]
            where_clause will look like ((name>%s and url=%s) or (type <= %s))
            items within each dictionary get 'AND'-ed and dictionaries themselves get 'OR'-ed

        Returns:
            an integer indicating count of rows deleted

        """
        keys = cls._COMMA.join(values.keys())
        value_place_holder = cls._PLACEHOLDER * len(values)
        where_clause, where_values = cls._get_where_clause_with_values(where_keys)
        query = cls._update_string.format(table, keys, value_place_holder[:-1], where_clause)
        yield from cur.execute(query, (tuple(values.values()) + where_values))
        return (yield from cur.fetchall())