def purge_keys(self):
        """
        Deletes all SSH keys on the localhost associated with the current remote host.
        """
        r = self.local_renderer
        r.env.default_ip = self.hostname_to_ip(self.env.default_hostname)
        r.env.home_dir = '/home/%s' % getpass.getuser()
        r.local('ssh-keygen -f "{home_dir}/.ssh/known_hosts" -R {host_string}')
        if self.env.default_hostname:
            r.local('ssh-keygen -f "{home_dir}/.ssh/known_hosts" -R {default_hostname}')
        if r.env.default_ip:
            r.local('ssh-keygen -f "{home_dir}/.ssh/known_hosts" -R {default_ip}')