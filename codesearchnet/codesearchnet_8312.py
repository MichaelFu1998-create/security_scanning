def exists(self):
        """ Check if the database table exists
        """
        query = (
            "SELECT name FROM sqlite_master " + "WHERE type='table' AND name=?",
            (self.__tablename__,),
        )
        connection = sqlite3.connect(self.sqlite_file)
        cursor = connection.cursor()
        cursor.execute(*query)
        return True if cursor.fetchone() else False