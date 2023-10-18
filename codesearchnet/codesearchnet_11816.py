def exists(self, name='default', site=None, use_root=False):
        """
        Returns true if a database with the given name exists. False otherwise.
        """

        r = self.database_renderer(name=name, site=site)

        if int(use_root):
            kwargs = dict(
                db_user=r.env.get('db_root_username', 'postgres'),
                db_password=r.env.get('db_root_password', 'password'),
                db_host=r.env.db_host,
                db_name=r.env.db_name,
            )
            r.env.update(kwargs)

        # Set pgpass file.
        if r.env.db_password:
            self.write_pgpass(name=name, root=use_root)

#        cmd = ('psql --username={db_user} --no-password -l '\
#            '--host={db_host} --dbname={db_name}'\
#            '| grep {db_name} | wc -l').format(**env)

        ret = None
        with settings(warn_only=True):
            ret = r.run('psql --username={db_user} --host={db_host} -l '\
            '| grep {db_name} | wc -l')
            if ret is not None:
                if 'password authentication failed' in ret:
                    ret = False
                else:
                    ret = int(ret) >= 1

        if ret is not None:
            print('%s database on site %s %s exist' % (name, self.genv.SITE, 'DOES' if ret else 'DOES NOT'))
            return ret