def install_auth_basic_user_file(self, site=None):
        """
        Installs users for basic httpd auth.
        """
        r = self.local_renderer

        hostname = self.current_hostname

        target_sites = self.genv.available_sites_by_host.get(hostname, None)

        for _site, site_data in self.iter_sites(site=site, setter=self.set_site_specifics):
            if self.verbose:
                print('~'*80, file=sys.stderr)
                print('Site:', _site, file=sys.stderr)
                print('env.apache_auth_basic:', r.env.auth_basic, file=sys.stderr)

            # Only load site configurations that are allowed for this host.
            if target_sites is not None:
                assert isinstance(target_sites, (tuple, list))
                if _site not in target_sites:
                    continue

            if not r.env.auth_basic:
                continue

            assert r.env.auth_basic_users, 'No apache auth users specified.'
            for username, password in r.env.auth_basic_users:
                r.env.auth_basic_username = username
                r.env.auth_basic_password = password
                r.env.apache_site = _site
                r.env.fn = r.format(r.env.auth_basic_authuserfile)
                if self.files.exists(r.env.fn):
                    r.sudo('htpasswd -b {fn} {auth_basic_username} {auth_basic_password}')
                else:
                    r.sudo('htpasswd -b -c {fn} {auth_basic_username} {auth_basic_password}')