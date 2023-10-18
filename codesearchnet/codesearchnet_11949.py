def shell(self, name='default', site=None, use_root=0, **kwargs):
        """
        Opens a SQL shell to the given database, assuming the configured database
        and user supports this feature.
        """
        r = self.database_renderer(name=name, site=site)

        if int(use_root):
            kwargs = dict(
                db_user=r.env.db_root_username,
                db_password=r.env.db_root_password,
                db_host=r.env.db_host,
                db_name=r.env.db_name,
            )
            r.env.update(kwargs)

        if not name:
            r.env.db_name = ''

        r.run('/bin/bash -i -c "mysql -u {db_user} -p\'{db_password}\' -h {db_host} {db_name}"')