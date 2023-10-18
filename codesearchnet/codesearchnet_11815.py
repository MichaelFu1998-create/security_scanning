def dumpload(self, site=None, role=None):
        """
        Dumps and loads a database snapshot simultaneously.
        Requires that the destination server has direct database access
        to the source server.

        This is better than a serial dump+load when:
        1. The network connection is reliable.
        2. You don't need to save the dump file.

        The benefits of this over a dump+load are:
        1. Usually runs faster, since the load and dump happen in parallel.
        2. Usually takes up less disk space since no separate dump file is
            downloaded.
        """
        r = self.database_renderer(site=site, role=role)
        r.run('pg_dump -c --host={host_string} --username={db_user} '
            '--blobs --format=c {db_name} -n public | '
            'pg_restore -U {db_postgresql_postgres_user} --create '
            '--dbname={db_name}')