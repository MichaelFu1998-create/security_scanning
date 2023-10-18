def items(self):
        """ returns all items off the store as tuples
        """
        query = "SELECT {}, {} from {}".format(
            self.__key__, self.__value__, self.__tablename__
        )
        connection = sqlite3.connect(self.sqlite_file)
        cursor = connection.cursor()
        cursor.execute(query)
        r = []
        for key, value in cursor.fetchall():
            r.append((key, value))
        return r