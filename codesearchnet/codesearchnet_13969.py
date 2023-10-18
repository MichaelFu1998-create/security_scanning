def find(self, q, operator="=", fields="*", key=None):
        
        """A simple SQL SELECT query.
        
        Retrieves all rows from the table 
        where the given query value is found in the given column (primary key if None).
        A different comparison operator (e.g. >, <, like) can be set.
        The wildcard character is * and automatically sets the operator to "like".
        Optionally, the fields argument can be a list of column names to select.
        Returns a list of row tuples containing fields.
        
        """
        
        if key == None: key = self._key
        if fields != "*": fields = ", ".join(fields)
        try: q = unicode(q)
        except: pass
        if q != "*" and (q[0] == "*" or q[-1] == "*"):
            if q[0]  == "*": q = "%"+q.lstrip("*")
            if q[-1] == "*": q = q.rstrip("*")+"%"
            operator = "like"
        
        if q != "*":
            sql = "select "+fields+" from "+self._name+" where "+key+" "+operator+" ?"
            self._db._cur.execute(sql, (q,))
        else:
            sql = "select "+fields+" from "+self._name
            self._db._cur.execute(sql)
        
        # You need to watch out here when bad unicode data 
        # has entered the database: pysqlite will throw an OperationalError.
        # http://lists.initd.org/pipermail/pysqlite/2006-April/000488.html
        matches = []
        for r in self._db._cur: matches.append(r)
        return matches