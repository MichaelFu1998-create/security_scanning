def create(self, name, overwrite=True):
        
        """Creates an SQLite database file.
        
        Creates an SQLite database with the given name.
        The .box file extension is added automatically.
        Overwrites any existing database by default.
        
        """
        
        self._name = name.rstrip(".db")
        from os import unlink
        if overwrite: 
            try: unlink(self._name + ".db")
            except: pass       
        self._con = sqlite.connect(self._name + ".db")
        self._cur = self._con.cursor()