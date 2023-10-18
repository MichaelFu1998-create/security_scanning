def rename(self, from_name, to_name):
        """Renames an existing database."""
        log.info('renaming database from %s to %s' % (from_name, to_name))
        self._run_stmt('alter database %s rename to %s' % (from_name, to_name))