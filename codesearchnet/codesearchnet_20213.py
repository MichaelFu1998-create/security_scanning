def lookup(self, username=None, reponame=None, key=None):
        """
        Lookup all available repos
        """
        if key is None:
            key = self.key(username, reponame)
        if key not in self.repos:
            raise UnknownRepository()

        return self.repos[key]