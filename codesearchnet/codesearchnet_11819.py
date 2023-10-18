def drop_database(self, name):
        """
        Delete a PostgreSQL database.

        Example::

            import burlap

            # Remove DB if it exists
            if burlap.postgres.database_exists('myapp'):
                burlap.postgres.drop_database('myapp')

        """
        with settings(warn_only=True):
            self.sudo('dropdb %s' % (name,), user='postgres')