def delete(cls, cur, table: str, where_keys: list):
        """
        Creates a delete query with where keys
        Supports multiple where clause with and or or both

        Args:
            table: a string indicating the name of the table
            where_keys: list of dictionary
            example of where keys: [{'name':('>', 'cip'),'url':('=', 'cip.com'},{'type':{'<=', 'manufacturer'}}]
            where_clause will look like ((name>%s and url=%s) or (type <= %s))
            items within each dictionary get 'AND'-ed and dictionaries themselves get 'OR'-ed

        Returns:
            an integer indicating count of rows deleted

        """
        where_clause, values = cls._get_where_clause_with_values(where_keys)
        query = cls._delete_query.format(table, where_clause)
        yield from cur.execute(query, values)
        return cur.rowcount