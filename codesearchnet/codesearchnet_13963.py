def connect(self, name):
        
        """Generic database.
        
        Opens the SQLite database with the given name.
        The .db extension is automatically appended to the name.
        For each table in the database an attribute is created,
        and assigned a Table object.
        
        You can do: database.table or database[table].
        
        """
        
        self._name = name.rstrip(".db")
        self._con = sqlite.connect(self._name + ".db")
        self._cur = self._con.cursor()
 
        self._tables = []
        self._cur.execute("select name from sqlite_master where type='table'")
        for r in self._cur: self._tables.append(r[0])
        
        self._indices = []
        self._cur.execute("select name from sqlite_master where type='index'")
        for r in self._cur: self._indices.append(r[0])
        
        for t in self._tables:
            self._cur.execute("pragma table_info("+t+")")
            fields = []
            key = ""
            for r in self._cur:
                fields.append(r[1])
                if r[2] == "integer": key = r[1]
            setattr(self, t, Table(self, t, key, fields))