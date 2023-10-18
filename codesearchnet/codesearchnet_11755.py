def virtualenv_exists(self, virtualenv_dir=None):
        """
        Returns true if the virtual environment has been created.
        """
        r = self.local_renderer
        ret = True
        with self.settings(warn_only=True):
            ret = r.run_or_local('ls {virtualenv_dir}') or ''
            ret = 'cannot access' not in ret.strip().lower()

        if self.verbose:
            if ret:
                print('Yes')
            else:
                print('No')

        return ret