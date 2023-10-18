def connection_url(self, name=None):
        """
        Provides a connection string for database as a sqlalchemy compatible URL.

        NB - this doesn't include special arguments related to SSL connectivity (which are outside the scope
        of the connection URL format).

        Parameters
        ----------
        name: str, optional
            an override database name for the connection string.

        Returns
        -------
        str: the connection URL (e.g. postgresql://user1@localhost:5432/db1)
            """
        return 'postgresql://{user}@{host}:{port}/{dbname}'.format(**{k: v for k, v in self._connect_options(name)})