def lock(self):
        """
        Marks the remote server as currently being deployed to.
        """
        self.init()
        r = self.local_renderer
        if self.file_exists(r.env.lockfile_path):
            raise exceptions.AbortDeployment('Lock file %s exists. Perhaps another deployment is currently underway?' % r.env.lockfile_path)
        else:
            self.vprint('Locking %s.' % r.env.lockfile_path)
            r.env.hostname = socket.gethostname()
            r.run_or_local('echo "{hostname}" > {lockfile_path}')