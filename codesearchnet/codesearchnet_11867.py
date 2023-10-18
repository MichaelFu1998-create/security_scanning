def set_root_login(self, r):
        """
        Looks up the root login for the given database on the given host and sets
        it to environment variables.

        Populates these standard variables:

            db_root_password
            db_root_username

        """

        # Check the legacy password location.
        try:
            r.env.db_root_username = r.env.root_username
        except AttributeError:
            pass
        try:
            r.env.db_root_password = r.env.root_password
        except AttributeError:
            pass

        # Check the new password location.
        key = r.env.get('db_host')
        if self.verbose:
            print('db.set_root_login.key:', key)
            print('db.set_root_logins:', r.env.root_logins)
        if key in r.env.root_logins:
            data = r.env.root_logins[key]
#             print('data:', data)
            if 'username' in data:
                r.env.db_root_username = data['username']
                r.genv.db_root_username = data['username']
            if 'password' in data:
                r.env.db_root_password = data['password']
                r.genv.db_root_password = data['password']
        else:
            msg = 'Warning: No root login entry found for host %s in role %s.' % (r.env.get('db_host'), self.genv.get('ROLE'))
            print(msg, file=sys.stderr)