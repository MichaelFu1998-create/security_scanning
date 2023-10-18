def write_pgpass(self, name=None, site=None, use_sudo=0, root=0):
        """
        Write the file used to store login credentials for PostgreSQL.
        """

        r = self.database_renderer(name=name, site=site)

        root = int(root)

        use_sudo = int(use_sudo)

        r.run('touch {pgpass_path}')
        if '~' in r.env.pgpass_path:
            r.run('chmod {pgpass_chmod} {pgpass_path}')
        else:
            r.sudo('chmod {pgpass_chmod} {pgpass_path}')

        if root:
            r.env.shell_username = r.env.get('db_root_username', 'postgres')
            r.env.shell_password = r.env.get('db_root_password', 'password')
        else:
            r.env.shell_username = r.env.db_user
            r.env.shell_password = r.env.db_password

        r.append(
            '{db_host}:{port}:*:{shell_username}:{shell_password}',
            r.env.pgpass_path,
            use_sudo=use_sudo)