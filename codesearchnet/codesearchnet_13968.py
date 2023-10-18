def sql(self, sql):
        
        """ Executes a raw SQL statement on the database.
        """
        
        self._cur.execute(sql)
        if sql.lower().find("select") >= 0:
            matches = []
            for r in self._cur: matches.append(r)
            return matches