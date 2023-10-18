def uncommented_lines(self, filename, use_sudo=False):
        """
        Get the lines of a remote file, ignoring empty or commented ones
        """
        func = run_as_root if use_sudo else self.run
        res = func('cat %s' % quote(filename), quiet=True)
        if res.succeeded:
            return [line for line in res.splitlines() if line and not line.startswith('#')]
        return []