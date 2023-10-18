def pip(self, package_names, raise_on_error=True):
        """
        Install specified python packages using pip. -U option added
        Waits for command to finish.

        Parameters
        ----------
        package_names: list-like of str
        raise_on_error: bool, default True
            If True then raise ValueError if stderr is not empty
        """
        if isinstance(package_names, basestring):
            package_names = [package_names]
        cmd = "pip install -U %s" % (' '.join(package_names))
        return self.wait(cmd, raise_on_error=raise_on_error)