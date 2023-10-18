def select(cls, cur, table: str, order_by: str, columns: list=None, where_keys: list=None, limit=100,
               offset=0):
        """
        Creates a select query for selective columns with where keys
        Supports multiple where claus with and or or both

        Args:
            table: a string indicating the name of the table
            order_by: a string indicating column name to order the results on
            columns: list of columns to select from
            where_keys: list of dictionary
            limit: the limit on the number of results
            offset: offset on the results

            example of where keys: [{'name':('>', 'cip'),'url':('=', 'cip.com'},{'type':{'<=', 'manufacturer'}}]
            where_clause will look like ((name>%s and url=%s) or (type <= %s))
            items within each dictionary get 'AND'-ed and across dictionaries get 'OR'-ed

        Returns:
            A list of 'Record' object with table columns as properties

        """
        if columns:
            columns_string = cls._COMMA.join(columns)
            if where_keys:
                where_clause, values = cls._get_where_clause_with_values(where_keys)
                query = cls._select_selective_column_with_condition.format(columns_string, table, where_clause,
                                                                           order_by, limit, offset)
                q, t = query, values
            else:
                query = cls._select_selective_column.format(columns_string, table, order_by, limit, offset)
                q, t = query, ()
        else:
            if where_keys:
                where_clause, values = cls._get_where_clause_with_values(where_keys)
                query = cls._select_all_string_with_condition.format(table, where_clause, order_by, limit, offset)
                q, t = query, values
            else:
                query = cls._select_all_string.format(table, order_by, limit, offset)
                q, t = query, ()

        yield from cur.execute(q, t)
        return (yield from cur.fetchall())