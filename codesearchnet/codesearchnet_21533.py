def dump(self, name, filename):
        """
        Saves the state of a database to a file.

        Parameters
        ----------
        name: str
            the database to be backed up.
        filename: str
            path to a file where database backup will be written.
        """
        if not self.exists(name):
            raise DatabaseError('database %s does not exist!')
        log.info('dumping %s to %s' % (name, filename))
        self._run_cmd('pg_dump', '--verbose', '--blobs', '--format=custom',
                      '--file=%s' % filename, name)