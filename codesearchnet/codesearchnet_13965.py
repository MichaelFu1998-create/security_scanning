def create_table(self, name, fields=[], key="id"):
        
        """Creates a new table.
        
        Creates a table with the given name,
        containing the list of given fields.
        Since SQLite uses manifest typing, no data type need be supplied.
        The primary key is "id" by default,
        an integer that can be set or otherwise autoincrements.
        
        """
        
        for f in fields: 
            if f == key: fields.remove(key)
        sql  = "create table "+name+" "
        sql += "("+key+" integer primary key"
        for f in fields: sql += ", "+f+" varchar(255)"
        sql += ")"
        self._cur.execute(sql)
        self._con.commit()
        self.index(name, key, unique=True)
        self.connect(self._name)