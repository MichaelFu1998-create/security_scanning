def bump(self, target):
        """
        Bumps the Version given a target

        The target can be either MAJOR, MINOR or PATCH
        """
        if target == 'patch':
            return Version(self.major, self.minor, self.patch + 1)
        if target == 'minor':
            return Version(self.major, self.minor + 1, 0)
        if target == 'major':
            return Version(self.major + 1, 0, 0)
        return self.clone()