def append(self, *args, **kw):
        
        """Adds a new row to a table.
        
        Adds a row to the given table.
        The column names and their corresponding values
        must either be supplied as a dictionary of {fields:values},
        or a series of keyword arguments of field=value style.
        
        """

        if args and kw: 
            return
        if args and type(args[0]) == dict:
            fields = [k for k in args[0]]
            v = [args[0][k] for k in args[0]]
        if kw:
            fields = [k for k in kw]
            v = [kw[k] for k in kw]
        
        q = ", ".join(["?" for x in fields])
        sql  = "insert into "+self._name+" ("+", ".join(fields)+") "
        sql += "values ("+q+")"
        self._db._cur.execute(sql, v)
        self._db._i += 1
        if self._db._i >= self._db._commit:
            self._db._i = 0
            self._db._con.commit()