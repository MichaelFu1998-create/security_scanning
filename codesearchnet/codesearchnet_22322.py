def get_current_branch(self):
        """Returns the currently active branch"""
        return next((self._sanitize(branch)
                     for branch in self._git.branch(color="never").splitlines()
                     if branch.startswith('*')),
                    None)