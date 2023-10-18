def query(self, sql_string, *args, **kwargs):
        """ 
        Execute a DML query 

        :sql_string:    An SQL string template
        :*args:         Arguments to be passed for query parameters.
        :commit:        Whether or not to commit the transaction after the query
        :returns:       Psycopg2 result
        """
        commit = None
        columns = None
        if kwargs.get('commit') is not None:
            commit = kwargs.pop('commit')
        if kwargs.get('columns') is not None:
            columns = kwargs.pop('columns')
        query = self._assemble_simple(sql_string, *args, **kwargs)
        return self._execute(query, commit=commit, working_columns=columns)