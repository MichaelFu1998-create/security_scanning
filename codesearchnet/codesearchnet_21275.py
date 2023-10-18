def _assemble_simple(self, sql_str, *args, **kwargs):
        """ 
        Format a select statement with specific columns 

        :sql_str:   An SQL string template
        :*args:     Arguments to use as query parameters.
        :returns:   Psycopg2 compiled query
        """
        
        query_string = sql.SQL(sql_str).format(
            *[sql.Literal(a) for a in args]
            )

        return query_string