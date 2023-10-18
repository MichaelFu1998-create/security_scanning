def create(self):  # pragma: no cover
        """ Create the new table in the SQLite database
        """
        query = (
            """
            CREATE TABLE {} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {} STRING(256),
                {} STRING(256)
            )"""
        ).format(self.__tablename__, self.__key__, self.__value__)
        connection = sqlite3.connect(self.sqlite_file)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()