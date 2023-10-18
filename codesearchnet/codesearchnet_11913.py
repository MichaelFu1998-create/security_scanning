def ssh_config(self, name=''):
        """
        Get the SSH parameters for connecting to a vagrant VM.
        """
        r = self.local_renderer
        with self.settings(hide('running')):
            output = r.local('vagrant ssh-config %s' % name, capture=True)

        config = {}
        for line in output.splitlines()[1:]:
            key, value = line.strip().split(' ', 2)
            config[key] = value
        return config