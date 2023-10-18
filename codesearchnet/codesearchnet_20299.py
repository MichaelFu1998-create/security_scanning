def apt(self, package_names, raise_on_error=False):
        """
        Install specified packages using apt-get. -y options are
        automatically used. Waits for command to finish.

        Parameters
        ----------
        package_names: list-like of str
        raise_on_error: bool, default False
            If True then raise ValueError if stderr is not empty
            debconf often gives tty error
        """
        if isinstance(package_names, basestring):
            package_names = [package_names]
        cmd = "apt-get install -y %s" % (' '.join(package_names))
        return self.wait(cmd, raise_on_error=raise_on_error)