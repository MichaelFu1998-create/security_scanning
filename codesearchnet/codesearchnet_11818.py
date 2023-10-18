def shell(self, name='default', site=None, **kwargs):
        """
        Opens a SQL shell to the given database, assuming the configured database
        and user supports this feature.
        """
        r = self.database_renderer(name=name, site=site)
        self.write_pgpass(name=name, site=site, root=True)

        db_name = kwargs.get('db_name')
        if db_name:
            r.env.db_name = db_name
            r.run('/bin/bash -i -c "psql --username={db_root_username} --host={db_host} --dbname={db_name}"')
        else:
            r.run('/bin/bash -i -c "psql --username={db_root_username} --host={db_host}"')