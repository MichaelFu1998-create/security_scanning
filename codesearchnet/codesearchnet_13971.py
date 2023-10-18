def edit(self, id, *args, **kw):
        
        """ Edits the row with given id.
        """
        
        if args and kw: 
            return
        if args and type(args[0]) == dict:
            fields = [k for k in args[0]]
            v = [args[0][k] for k in args[0]]
        if kw:
            fields = [k for k in kw]
            v = [kw[k] for k in kw]
        
        sql  = "update "+self._name+" set "+"=?, ".join(fields)+"=? where "+self._key+"="+unicode(id)
        self._db._cur.execute(sql, v)
        self._db._i += 1
        if self._db._i >= self._db._commit:
            self._db._i = 0
            self._db._con.commit()