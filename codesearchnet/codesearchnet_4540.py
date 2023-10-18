def makedirs(self, path, mode=511, exist_ok=False):
        """Create a directory on the remote side.

        If intermediate directories do not exist, they will be created.

        Parameters
        ----------
        path : str
            Path of directory on the remote side to create.
        mode : int
            Permissions (posix-style) for the newly-created directory.
        exist_ok : bool
            If False, raise an OSError if the target directory already exists.
        """
        if exist_ok is False and self.isdir(path):
            raise OSError('Target directory {} already exists'.format(path))

        self.execute_wait('mkdir -p {}'.format(path))
        self.sftp_client.chmod(path, mode)