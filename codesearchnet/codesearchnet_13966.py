def create_index(self, table, field, unique=False, ascending=True):
        
        """Creates a table index.
        
        Creates an index on the given table,
        on the given field with unique values enforced or not,
        in ascending or descending order.
        
        """
        
        if unique: u = "unique "
        else: u = ""
        if ascending: a = "asc"
        else: a = "desc"
        sql  = "create "+u+"index index_"+table+"_"+field+" "
        sql += "on "+table+"("+field+" "+a+")"
        self._cur.execute(sql)
        self._con.commit()