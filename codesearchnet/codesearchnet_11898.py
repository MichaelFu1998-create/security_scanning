def configure_modevasive(self):
        """
        Installs the mod-evasive Apache module for combating DDOS attacks.

        https://www.linode.com/docs/websites/apache-tips-and-tricks/modevasive-on-apache
        """
        r = self.local_renderer
        if r.env.modevasive_enabled:
            self.install_packages()

            # Write conf for each Ubuntu version since they don't conflict.
            fn = r.render_to_file('apache/apache_modevasive.template.conf')

            # Ubuntu 12.04
            r.put(
                local_path=fn,
                remote_path='/etc/apache2/mods-available/mod-evasive.conf',
                use_sudo=True)

            # Ubuntu 14.04
            r.put(
                local_path=fn,
                remote_path='/etc/apache2/mods-available/evasive.conf',
                use_sudo=True)

            self.enable_mod('evasive')
        else:
#             print('self.last_manifest:', self.last_manifest)
#             print('a:', self.last_manifest.apache_modevasive_enabled)
#             print('b:', self.last_manifest.modevasive_enabled)
            if self.last_manifest.modevasive_enabled:
                self.disable_mod('evasive')