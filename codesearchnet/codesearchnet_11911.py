def get_current_commit(self):
        """
        Retrieves the git commit number of the current head branch.
        """
        with hide('running', 'stdout', 'stderr', 'warnings'):
            s = str(self.local('git rev-parse HEAD', capture=True))
            self.vprint('current commit:', s)
            return s