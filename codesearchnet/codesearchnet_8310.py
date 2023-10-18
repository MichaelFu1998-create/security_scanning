def delete(self, key):
        """ Delete a key from the store

            :param str value: Value
        """
        query = (
            "DELETE FROM {} WHERE {}=?".format(self.__tablename__, self.__key__),
            (key,),
        )
        connection = sqlite3.connect(self.sqlite_file)
        cursor = connection.cursor()
        cursor.execute(*query)
        connection.commit()