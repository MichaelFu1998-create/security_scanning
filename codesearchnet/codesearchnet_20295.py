def chdir(self, new_pwd, relative=True):
        """
        Parameters
        ----------
        new_pwd: str,
            Directory to change to
        relative: bool, default True
            If True then the given directory is treated as relative to the
            current directory
        """
        if new_pwd and self.pwd and relative:
            new_pwd = os.path.join(self.pwd, new_pwd)
        self.pwd = new_pwd