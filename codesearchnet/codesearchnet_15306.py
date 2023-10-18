def drop_all(self, check_first: bool = True):
        """Drop all tables from the database.

        :param bool check_first: Defaults to True, only issue DROPs for tables confirmed to be
          present in the target database. Defers to :meth:`sqlalchemy.sql.schema.MetaData.drop_all`
        """
        self._metadata.drop_all(self.engine, checkfirst=check_first)
        self._store_drop()