def configure(self, reboot=1):
        """
        Assigns a name to the server accessible from user space.

        Note, we add the name to /etc/hosts since not all programs use
        /etc/hostname to reliably identify the server hostname.
        """
        r = self.local_renderer
        for ip, hostname in self.iter_hostnames():
            self.vprint('ip/hostname:', ip, hostname)
            r.genv.host_string = ip
            r.env.hostname = hostname
            with settings(warn_only=True):
                r.sudo('echo "{hostname}" > /etc/hostname')
                r.sudo('echo "127.0.0.1 {hostname}" | cat - /etc/hosts > /tmp/out && mv /tmp/out /etc/hosts')
                r.sudo(r.env.set_hostname_command)
                if r.env.auto_reboot and int(reboot):
                    r.reboot()