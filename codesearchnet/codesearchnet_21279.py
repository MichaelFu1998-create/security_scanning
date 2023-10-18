def select(self, sql_string, cols, *args, **kwargs):
        """ 
        Execute a SELECT statement 

        :sql_string:    An SQL string template
        :columns:       A list of columns to be returned by the query
        :*args:         Arguments to be passed for query parameters.
        :returns:       Psycopg2 result
        """
        working_columns = None
        if kwargs.get('columns') is not None:
            working_columns = kwargs.pop('columns')
        query = self._assemble_select(sql_string, cols, *args, *kwargs)
        return self._execute(query, working_columns=working_columns)