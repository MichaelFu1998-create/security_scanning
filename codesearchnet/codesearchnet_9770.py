def get_main_database_path(self):
        """
        Should return the path to the database

        Returns
        -------
        path : unicode
            path to the database, empty string for in-memory databases
        """
        cur = self.conn.cursor()
        cur.execute("PRAGMA database_list")
        rows = cur.fetchall()
        for row in rows:
            if row[1] == str("main"):
                return row[2]