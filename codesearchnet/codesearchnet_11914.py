def version(self):
        """
        Get the Vagrant version.
        """
        r = self.local_renderer
        with self.settings(hide('running', 'warnings'), warn_only=True):
            res = r.local('vagrant --version', capture=True)
        if res.failed:
            return None
        line = res.splitlines()[-1]
        version = re.match(r'Vagrant (?:v(?:ersion )?)?(.*)', line).group(1)
        return tuple(_to_int(part) for part in version.split('.'))