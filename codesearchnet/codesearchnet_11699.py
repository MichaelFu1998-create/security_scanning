def getmtime(self, path, use_sudo=False):
        """
        Return the time of last modification of path.
        The return value is a number giving the number of seconds since the epoch

        Same as :py:func:`os.path.getmtime()`
        """
        func = use_sudo and run_as_root or self.run
        with self.settings(hide('running', 'stdout')):
            return int(func('stat -c %%Y "%(path)s" ' % locals()).strip())