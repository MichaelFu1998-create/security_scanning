def unlock(self):
        """
        Unmarks the remote server as currently being deployed to.
        """
        self.init()
        r = self.local_renderer
        if self.file_exists(r.env.lockfile_path):
            self.vprint('Unlocking %s.' % r.env.lockfile_path)
            r.run_or_local('rm -f {lockfile_path}')