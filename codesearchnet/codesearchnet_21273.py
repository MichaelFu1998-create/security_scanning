def _assemble_with_columns(self, sql_str, columns, *args, **kwargs):
        """ 
        Format a select statement with specific columns 

        :sql_str:   An SQL string template
        :columns:   The columns to be selected and put into {0}
        :*args:     Arguments to use as query parameters.
        :returns:   Psycopg2 compiled query
        """

        # Handle any aliased columns we get (e.g. table_alias.column)
        qcols = []
        for col in columns:
            if '.' in col:
                # Explodeded it
                wlist = col.split('.')

                # Reassemble into string and drop it into the list
                qcols.append(sql.SQL('.').join([sql.Identifier(x) for x in wlist]))
            else:
                qcols.append(sql.Identifier(col))

        # sql.SQL(', ').join([sql.Identifier(x) for x in columns]),
        
        query_string = sql.SQL(sql_str).format(
            sql.SQL(', ').join(qcols),
            *[sql.Literal(a) for a in args]
            )
        
        return query_string