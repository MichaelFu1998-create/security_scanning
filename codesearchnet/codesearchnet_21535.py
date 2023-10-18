def connection_dsn(self, name=None):
        """
        Provides a connection string for database.

        Parameters
        ----------
        name: str, optional
            an override database name for the connection string.

        Returns
        -------
        str: the connection string (e.g. 'dbname=db1 user=user1 host=localhost port=5432')
        """
        return ' '.join("%s=%s" % (param, value) for param, value in self._connect_options(name))