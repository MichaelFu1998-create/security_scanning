def isdir(self, path):
        """Return true if the path refers to an existing directory.

        Parameters
        ----------
        path : str
            Path of directory on the remote side to check.
        """
        result = True
        try:
            self.sftp_client.lstat(path)
        except FileNotFoundError:
            result = False

        return result