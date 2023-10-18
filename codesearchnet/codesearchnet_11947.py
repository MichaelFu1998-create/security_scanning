def exists(self, **kwargs):
        """
        Returns true if a database with the given name exists. False otherwise.
        """
        name = kwargs.pop('name', 'default')
        site = kwargs.pop('site', None)
        r = self.database_renderer(name=name, site=site)
        ret = r.run('mysql -h {db_host} -u {db_root_username} '\
            '-p"{db_root_password}" -N -B -e "SELECT IF(\'{db_name}\''\
            ' IN(SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA), '\
            '\'exists\', \'notexists\') AS found;"')
        if ret is not None:
            ret = 'notexists' not in (ret or 'notexists')
        if ret is not None:
            msg = '%s database on site %s %s exist.' \
                % (name.title(), env.SITE, 'DOES' if ret else 'DOES NOT')
            if ret:
                print(green(msg))
            else:
                print(red(msg))
            return ret