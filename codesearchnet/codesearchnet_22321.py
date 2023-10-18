def get_branches(self):
        """Returns a list of the branches"""
        return [self._sanitize(branch)
                for branch in self._git.branch(color="never").splitlines()]