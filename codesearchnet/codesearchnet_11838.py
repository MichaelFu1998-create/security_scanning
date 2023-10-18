def configure_bleeding(self):
        """
        Enables the repository for a most current version on Debian systems.

            https://www.rabbitmq.com/install-debian.html
        """
        lm = self.last_manifest
        r = self.local_renderer
        if self.env.bleeding and not lm.bleeding:
            # Install.
            r.append(
                text='deb http://www.rabbitmq.com/debian/ testing main',
                filename='/etc/apt/sources.list.d/rabbitmq.list',
                use_sudo=True)
            r.sudo('cd /tmp; wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc | sudo apt-key add -')
            r.sudo('apt-get update')

        elif not self.env.bleeding and lm.bleeding:
            # Uninstall.
            r.sudo('rm -f /etc/apt/sources.list.d/rabbitmq.list')
            r.sudo('apt-get update')