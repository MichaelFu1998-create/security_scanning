def create(self, username, groups=None, uid=None, create_home=None, system=False, password=None, home_dir=None):
        """
        Creates a user with the given username.
        """
        r = self.local_renderer
        r.env.username = username

        args = []

        if uid:
            args.append('-u %s' % uid)

        if create_home is None:
            create_home = not system

        if create_home is True:
            if home_dir:
                args.append('--home %s' % home_dir)
        elif create_home is False:
            args.append('--no-create-home')

        if password is None:
            pass
        elif password:
            crypted_password = _crypt_password(password)
            args.append('-p %s' % quote(crypted_password))
        else:
            args.append('--disabled-password')

        args.append('--gecos ""')

        if system:
            args.append('--system')

        r.env.args = ' '.join(args)
        r.env.groups = (groups or '').strip()
        r.sudo('adduser {args} {username} || true')
        if groups:
            for group in groups.split(' '):
                group = group.strip()
                if not group:
                    continue
                r.sudo('adduser %s %s || true' % (username, group))