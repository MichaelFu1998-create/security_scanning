def configure_site(self, full=1, site=None, delete_old=0):
        """
        Configures Apache to host one or more websites.
        """
        from burlap import service

        r = self.local_renderer

        print('Configuring Apache...', file=sys.stderr)

        site = site or self.genv.SITE

        if int(delete_old) and site == ALL:
            # Delete all existing enabled and available sites.
            r.sudo('rm -f {sites_available}/*')
            r.sudo('rm -f {sites_enabled}/*')

        if r.env.manage_site_conf:

            # Run an optional customizable command to clear or delete old sites before writing the new ones.
            if r.env.delete_site_command:
                r.sudo(r.env.delete_site_command)

            for _site, site_data in self.iter_sites(site=site, setter=self.set_site_specifics):
                r = self.local_renderer

                #r.env.site = site
                if self.verbose:
                    print('-'*80, file=sys.stderr)
                    print('Site:', _site, file=sys.stderr)
                    print('-'*80, file=sys.stderr)

                r.env.ssl = _site.endswith('_secure')
                r.env.apache_site = _site
                r.env.server_name = r.format(r.env.domain_template)

                # Write WSGI template
                if r.env.wsgi_enabled:
                    r.pc('Writing WSGI template for site %s...' % _site)
                    r.env.wsgi_scriptalias = r.format(r.env.wsgi_scriptalias)
                    fn = self.render_to_file(r.env.wsgi_template)
                    r.env.wsgi_dir = r.env.remote_dir = os.path.split(r.env.wsgi_scriptalias)[0]
                    r.sudo('mkdir -p {remote_dir}')
                    r.put(local_path=fn, remote_path=r.env.wsgi_scriptalias, use_sudo=True)

                # Write site configuration.
                r.pc('Writing site configuration for site %s...' % _site)
                r.env.auth_basic_authuserfile = r.format(self.env.auth_basic_authuserfile)
                r.env.ssl_certificates = list(self.iter_certificates())
                if r.env.server_aliases_template:
                    r.env.server_aliases = r.format(r.env.server_aliases_template)
                if r.env.domain_with_sub_template:
                    r.env.domain_with_sub = r.format(r.env.domain_with_sub_template)
                if r.env.domain_without_sub_template:
                    r.env.domain_without_sub = r.format(r.env.domain_without_sub_template)
                if r.env.domain_template:
                    r.env.domain = r.format(r.env.domain_template)
                genv = r.collect_genv()
                genv['current_hostname'] = self.current_hostname
                fn = self.render_to_file(
                    self.env.site_template,
                    extra=genv,
                    formatter=partial(r.format, ignored_variables=self.env.ignored_template_variables))
                r.env.site_conf = _site+'.conf'
                r.env.site_conf_fqfn = os.path.join(r.env.sites_available, r.env.site_conf)
                r.put(local_path=fn, remote_path=r.env.site_conf_fqfn, use_sudo=True)

                self.enable_site(_site)

                self.clear_local_renderer()

        self.enable_mods()

        if int(full):
            # Write master Apache configuration file.
            if r.env.manage_httpd_conf:
                fn = self.render_to_file('apache/apache_httpd.template.conf')
                r.put(local_path=fn, remote_path=r.env.conf, use_sudo=True)

            # Write Apache listening ports configuration.
            if r.env.manage_ports_conf:
                fn = self.render_to_file('apache/apache_ports.template.conf')
                r.put(local_path=fn, remote_path=r.env.ports_path, use_sudo=True)

        r.sudo('chown -R {apache_web_user}:{apache_web_group} {apache_root}')