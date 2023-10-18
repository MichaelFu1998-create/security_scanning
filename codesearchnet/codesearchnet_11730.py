def exists(self, name):
        """
        Check if a group exists.
        """
        with self.settings(hide('running', 'stdout', 'warnings'), warn_only=True):
            return self.run('getent group %(name)s' % locals()).succeeded