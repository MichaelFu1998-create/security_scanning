def _haveKey(self, key):
        """ Is the key `key` available?
        """
        query = (
            "SELECT {} FROM {} WHERE {}=?".format(
                self.__value__, self.__tablename__, self.__key__
            ),
            (key,),
        )
        connection = sqlite3.connect(self.sqlite_file)
        cursor = connection.cursor()
        cursor.execute(*query)
        return True if cursor.fetchone() else False