def restore(self, name, filename):
        """
        Loads state of a backup file to a database.

        Note
        ----
        If database name does not exist, it will be created.

        Parameters
        ----------
        name: str
            the database to which backup will be restored.
        filename: str
            path to a file contain a postgres database backup.
        """
        if not self.exists(name):
            self.create(name)
        else:
            log.warn('overwriting contents of database %s' % name)
        log.info('restoring %s from %s' % (name, filename))
        self._run_cmd('pg_restore', '--verbose', '--dbname=%s' % name, filename)