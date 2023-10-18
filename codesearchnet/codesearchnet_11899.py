def configure_modsecurity(self):
        """
        Installs the mod-security Apache module.

        https://www.modsecurity.org
        """
        r = self.local_renderer
        if r.env.modsecurity_enabled and not self.last_manifest.modsecurity_enabled:

            self.install_packages()

            # Write modsecurity.conf.
            fn = self.render_to_file('apache/apache_modsecurity.template.conf')
            r.put(local_path=fn, remote_path='/etc/modsecurity/modsecurity.conf', use_sudo=True)

            # Write OWASP rules.
            r.env.modsecurity_download_filename = '/tmp/owasp-modsecurity-crs.tar.gz'
            r.sudo('cd /tmp; wget --output-document={apache_modsecurity_download_filename} {apache_modsecurity_download_url}')
            r.env.modsecurity_download_top = r.sudo(
                "cd /tmp; "
                "tar tzf %(apache_modsecurity_download_filename)s | sed -e 's@/.*@@' | uniq" % self.genv)
            r.sudo('cd /tmp; tar -zxvf %(apache_modsecurity_download_filename)s' % self.genv)
            r.sudo('cd /tmp; cp -R %(apache_modsecurity_download_top)s/* /etc/modsecurity/' % self.genv)
            r.sudo('mv /etc/modsecurity/modsecurity_crs_10_setup.conf.example  /etc/modsecurity/modsecurity_crs_10_setup.conf')

            r.sudo('rm -f /etc/modsecurity/activated_rules/*')
            r.sudo('cd /etc/modsecurity/base_rules; '
                'for f in * ; do ln -s /etc/modsecurity/base_rules/$f /etc/modsecurity/activated_rules/$f ; done')
            r.sudo('cd /etc/modsecurity/optional_rules; '
                'for f in * ; do ln -s /etc/modsecurity/optional_rules/$f /etc/modsecurity/activated_rules/$f ; done')

            r.env.httpd_conf_append.append('Include "/etc/modsecurity/activated_rules/*.conf"')

            self.enable_mod('evasive')
            self.enable_mod('headers')
        elif not self.env.modsecurity_enabled and self.last_manifest.modsecurity_enabled:
            self.disable_mod('modsecurity')